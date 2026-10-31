#!/bin/bash
#SBATCH --job-name=owi-rag-index
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
# Chunk + embed on a GPU node (sentence-transformers uses CUDA when present).
# Prerequisite: a venv with `pip install ".[ml]"` and data/docs.jsonl in place.
set -euo pipefail
source "${OWI_VENV:-$HOME/.venv/owi-rag}/bin/activate"
python -m owi_rag index
