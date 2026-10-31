FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
COPY owi_rag owi_rag
# CPU torch: the API only embeds queries; GPU embedding runs via slurm/index.sbatch
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir ".[ml,crawl]"
ENV OWI_DATA=/app/data
CMD ["uvicorn", "owi_rag.api:app", "--host", "0.0.0.0", "--port", "8000"]
