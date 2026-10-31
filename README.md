# owi-rag

Agentic RAG over [Open Web Index](https://openwebsearch.eu) data. Questions are split into sub-queries,
answered from a hybrid (BM25 + dense, fused with RRF) index, re-queried up to 3 rounds when the evidence
is thin, and answered with inline chunk citations. A plain-Python state machine, no LangChain.

```
OWI parquet -> ingest -> chunks -> BM25 (bm25s) ──┐
                                 -> dense (e5-small, FAISS) ─┴─ RRF -> agent loop -> cited answer
```

## Quickstart

1. Get data into `./data/parquet/` (see below), or write seed URLs to `./data/seeds.txt`.
2. Start the stack and pull the model:
   ```
   docker compose up -d
   make model
   make index          # or: make crawl-index
   curl -X POST localhost:8000/ask -H 'content-type: application/json' -d '{"question": "..."}'
   curl 'localhost:8000/search?q=...&mode=hybrid'
   ```
   `/ask` returns `answer` (cites chunks as `[id]`), `sources` (id -> URL) and `rounds`.

   The bundled Ollama container only gets a GPU on NVIDIA hosts. Otherwise run Ollama on the host and
   start the API with `OWI_LLM_URL=http://host.docker.internal:11434/v1 docker compose up -d api`.

### Getting OWI data

Install `owilix` (Linux/macOS, Python 3.11):
`curl -fsSL https://openwebindex.net/owilix/install.sh | sh`, then `owilix remote doctor`,
`owilix remote ls all` and `owilix remote pull <selector>` (see the
[owilix tutorial](https://openwebindex.eu/book/content/howto/b_data_download_with_owilix.html)).
Pick a small single-language partition and copy its `.parquet` files to `data/parquet/`.
`ingest` looks for a URL column (`url`/`uri`/`warc_target_uri`) and a text column
(`plain_text`/`text`/`content`/`body`) and stops with the column list if it finds neither;
override with `--url-col`/`--text-col`. **The column names are unverified against a real partition.**

Fallback if OWI access is blocked: `make crawl-index` crawls from `data/seeds.txt` with
`trafilatura`, honouring robots.txt. If you use it, say so here.

## Evaluation

**Data note:** the current index was built with the crawl fallback (`make crawl-index`) over the Python
tutorial and the SQLite docs (732 pages, 4,748 chunks), not Open Web Index data, because `owilix` was not
usable on the development machine.

`eval/questions.jsonl` holds 50 questions, `{"question": "...", "gold_urls": ["https://..."]}`. They were
drafted by an LLM and each gold page was checked to contain the answer's key terms; they have **not** been
reviewed by a human yet. Gold lists are usually one page, though other pages (e.g. the SQLite C API pages)
often repeat a fact, so recall is likely understated. Run `make eval`. It prints Recall@10 and nDCG@10
(distinct document URLs) for bm25, dense, hybrid and hybrid+agentic, plus LLM-judge citation
faithfulness, and writes `faithfulness.json`; check 20 of those judgments by hand.

| method | Recall@10 | nDCG@10 |
|---|---|---|
| bm25 | 0.960 | 0.842 |
| dense | 1.000 | 0.902 |
| hybrid | 1.000 | 0.890 |
| hybrid + agentic | 1.000 | 0.889 |

Citation faithfulness (share of answer sentences supported by the chunk they cite; uncited sentences
count as unsupported):

| answers | sentences (uncited) | qwen2.5:7b judge (eval code) | Gemini 4 Argon judge (by hand) |
|---|---|---|---|
| v1: Ollama default context, loose citation prompt | 112 (16) | 0.759 | 0.580 |
| v2: 16k context, cite-every-sentence prompt (current) | 131 (11) | 0.809 | **0.664** |
| v3: v2 + `bge-reranker-base` top-8 evidence (not kept) | 128 (13) | 0.805 | 0.688 |

v1 was silently truncated: Ollama's default ~2k-token context cut the evidence off most answer
prompts, so the model cited chunks it never saw. `docker-compose.yml` now sets
`OLLAMA_CONTEXT_LENGTH=16384`; set the same on a host Ollama.

v3 gained 2.4 points under Gemini, within noise at ~130 sentences (±4), at the cost of ~10 s per
answer on CPU and a 1 GB model, so the reranker was removed.

Which judge to trust: on 20 random v1 sentences checked by hand
([eval/v1/handcheck.md](eval/v1/handcheck.md)), Gemini agreed with the human on 19/20, qwen on 15/20,
and qwen's misses were mostly over-crediting its own answers. So the Gemini column is the better
estimate. The Gemini runs were done by hand in the Gemini app (2026-10-30), not by the eval code:
prompts, raw replies and the judged answers for each run are in [eval/v1/](eval/v1/),
[eval/v2/](eval/v2/) and [eval/v3/](eval/v3/). To run a hosted judge through
the API instead, export `OWI_JUDGE_URL`, `OWI_JUDGE_KEY` and `OWI_JUDGE_MODEL` (see `owi_rag/llm.py`)
and run the eval outside Docker: `python -m owi_rag.eval eval/questions.jsonl --faith`
(`make eval` does not pass these variables into the container).

### Limitations
- Tiny two-site corpus; the 50 questions are LLM-drafted from knowledge of those docs, so the eval set is small, easy and biased toward what the drafter knew. Recall@10 is saturated (1.0 for three of four methods), so it cannot separate them; nDCG@10 differences are small at n=50.
- The default LLM judge is the model that wrote the answers and over-credits them (see above). The hand check is only 20 sentences, so judge-agreement numbers are rough.
- About a third of answer sentences are still not supported by what they cite (Gemini judge), and 11 of 131 have no citation. The hand check covers v1 answers only.
- The agentic ranking is retrieval order across rounds, not a global score, so it is not strictly comparable to the single-shot rankings.
- Chunk size counts words (220 ≈ 300 tokens), not tokens. No source-diversity signal.
- Not built yet: an agent fleet (parallel worker agents per sub-question, or OURRS-style published agent opinions). It would need multi-hop eval questions to show any gain; planned as a separate project.

## Scaling
Shard the FAISS/BM25 indexes by partition and fuse at query time; run embedding as a Slurm job
(`slurm/index.sbatch`) or Spark; swap Ollama for vLLM via `OWI_LLM_URL`; the Helm chart
(`helm/owi-rag`) deploys the API against a PVC holding the built indexes. It does not deploy the LLM;
in the same namespace, the [otwld Ollama chart](https://github.com/otwld/ollama-helm) with release name
`ollama` matches the default `llmUrl`:
```
helm repo add otwld https://helm.otwld.com/
helm install ollama otwld/ollama --set 'ollama.models.pull={qwen2.5:7b-instruct}'
helm install rag helm/owi-rag
```
On a GPU node, add `--set ollama.gpu.enabled=true`, or point `llmUrl` at a vLLM server instead. Ingest reads the same
Parquet layout the OWI pipeline publishes, so it can sit downstream of it.

## Development
`pip install -e ".[ml,crawl]" pytest ruff && ruff check . && pytest` (CI runs the same, without the heavy extras).
