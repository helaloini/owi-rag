RUN = docker compose run --rm api python -m owi_rag

# put OWI parquet files (or a seeds.txt for the crawl fallback) under ./data first, see README
model:
	docker compose exec ollama ollama pull qwen2.5:7b-instruct

index:
	$(RUN) ingest data/parquet
	$(RUN) index

crawl-index:
	$(RUN) crawl data/seeds.txt
	$(RUN) index

eval:
	docker compose run --rm api python -m owi_rag.eval eval/questions.jsonl --faith
