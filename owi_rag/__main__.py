import argparse

p = argparse.ArgumentParser(prog="owi_rag")
sub = p.add_subparsers(dest="cmd", required=True)
a = sub.add_parser("ingest", help="OWI parquet dir -> data/docs.jsonl")
a.add_argument("src")
a.add_argument("--url-col")
a.add_argument("--text-col")
c = sub.add_parser("crawl", help="fallback: crawl from a file of seed URLs -> data/docs.jsonl")
c.add_argument("seeds")
c.add_argument("--per-seed", type=int, default=500)
sub.add_parser("index", help="data/docs.jsonl -> BM25 + FAISS")
args = p.parse_args()

if args.cmd == "ingest":
    from .ingest import from_parquet

    from_parquet(args.src, "data/docs.jsonl", args.url_col, args.text_col)
elif args.cmd == "crawl":
    from .ingest import from_crawl

    from_crawl(args.seeds, "data/docs.jsonl", args.per_seed)
else:
    from .index import build

    build()
