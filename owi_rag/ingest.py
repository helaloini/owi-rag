"""Write docs.jsonl ({"url", "text"} per line) from OWI Parquet files or a small crawl."""
import json
import urllib.robotparser
from pathlib import Path
from urllib.parse import urlparse

URL_COLS = ("url", "uri", "warc_target_uri")
TEXT_COLS = ("plain_text", "text", "content", "body")


def _pick(names, candidates):
    lower = {n.lower(): n for n in names}
    for c in candidates:
        if c in lower:
            return lower[c]
    raise SystemExit(f"none of {candidates} in parquet columns: {list(names)}. Pass --url-col/--text-col.")


def from_parquet(src, out, url_col=None, text_col=None):
    import pyarrow.parquet as pq

    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for path in sorted(Path(src).rglob("*.parquet")):
            pf = pq.ParquetFile(path)
            names = pf.schema_arrow.names
            u, t = url_col or _pick(names, URL_COLS), text_col or _pick(names, TEXT_COLS)
            for batch in pf.iter_batches(columns=[u, t], batch_size=1000):
                for url, text in zip(batch.column(u).to_pylist(), batch.column(t).to_pylist()):
                    if url and text and text.strip():
                        f.write(json.dumps({"url": url, "text": text}) + "\n")
                        n += 1
    print(f"{n} docs -> {out}")


def from_crawl(seeds, out, per_seed=500):
    # fallback when OWI access is blocked: say so in the README
    from trafilatura import extract, fetch_url
    from trafilatura.spider import focused_crawler

    robots = {}

    def allowed(url):
        p = urlparse(url)
        if p.netloc not in robots:
            rp = urllib.robotparser.RobotFileParser(f"{p.scheme}://{p.netloc}/robots.txt")
            try:
                rp.read()
            except OSError:
                rp = None
            robots[p.netloc] = rp
        rp = robots[p.netloc]
        return rp is None or rp.can_fetch("owi-rag", url)

    n, seen = 0, set()
    with open(out, "w", encoding="utf-8") as f:
        for seed in Path(seeds).read_text().split():
            _, links = focused_crawler(seed, max_seen_urls=per_seed)
            for url in {u.split("#")[0] for u in links} - seen:
                seen.add(url)
                if not allowed(url):
                    continue
                html = fetch_url(url)
                text = html and extract(html)
                if text:
                    f.write(json.dumps({"url": url, "text": text}) + "\n")
                    n += 1
    print(f"{n} docs -> {out}")
