import os

from openai import OpenAI


def _client(url, key, model, retries=2):
    c = OpenAI(base_url=url, api_key=key, max_retries=retries)

    def chat(prompt):
        r = c.chat.completions.create(model=model, temperature=0,
                                      messages=[{"role": "user", "content": prompt}])
        return r.choices[0].message.content

    return chat


# Ollama by default; point OWI_LLM_URL at a vLLM server to swap.
URL = os.getenv("OWI_LLM_URL", "http://localhost:11434/v1")
KEY = os.getenv("OWI_LLM_KEY", "none")
MODEL = os.getenv("OWI_LLM_MODEL", "qwen2.5:7b-instruct")
chat = _client(URL, KEY, MODEL)

# Faithfulness judge; set these to use a different model family than the one answering, e.g. Gemini
# via https://generativelanguage.googleapis.com/v1beta/openai/
JUDGE_MODEL = os.getenv("OWI_JUDGE_MODEL", MODEL)
# hosted judges return 503 when overloaded; retry with backoff rather than lose a long eval run
judge = _client(os.getenv("OWI_JUDGE_URL", URL), os.getenv("OWI_JUDGE_KEY", KEY), JUDGE_MODEL,
                retries=10)
