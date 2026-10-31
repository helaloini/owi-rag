"""Agentic loop as a plain state machine: DECOMPOSE -> RETRIEVE -> CHECK -(loop)-> ANSWER."""
import json
import re

DECOMPOSE = """Split the question into 1-3 short search queries. Reply with JSON only: {{"queries": [...]}}
Question: {q}"""

CHECK = """Question: {q}

Evidence:
{ev}

Is the evidence enough to answer the question? If not, give 1-3 new search queries that would find
what is missing. Reply with JSON only: {{"enough": true|false, "queries": [...]}}"""

ANSWER = """Evidence:
{ev}

Using only the evidence above, answer this question in 2-5 plain sentences: {q}
Cite after EVERY sentence, not once at the end: each sentence ends with the id of the chunk that
states it, in square brackets, e.g. "Lists are mutable [4-1]. Tuples are immutable [12-3]."
Only cite a chunk that actually says what the sentence claims; leave out claims no chunk states.
No headings, no lists. If the evidence is not enough, say so."""


def _json(text):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    try:
        return json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return {}


def _queries(parsed, fallback):
    qs = [q for q in parsed.get("queries", []) if isinstance(q, str) and q.strip()]
    return qs or fallback


def _fmt(chunks):
    return "\n\n".join(f"[{c['id']}] ({c['url']})\n{c['text']}" for c in chunks)


def ask(question, retriever, llm, max_rounds=3, k=5):
    state, queries, evidence, rounds, answer = "DECOMPOSE", [], {}, 0, ""
    while state != "DONE":
        if state == "DECOMPOSE":
            queries = _queries(_json(llm(DECOMPOSE.format(q=question))), [question])
            state = "RETRIEVE"
        elif state == "RETRIEVE":
            rounds += 1
            for q in queries:
                for c in retriever.search("hybrid", q, k):
                    evidence.setdefault(c["id"], c)
            state = "CHECK" if rounds < max_rounds else "ANSWER"
        elif state == "CHECK":
            v = _json(llm(CHECK.format(q=question, ev=_fmt(evidence.values()))))
            new = _queries(v, [])
            if v.get("enough") or not new:
                state = "ANSWER"
            else:
                queries, state = new, "RETRIEVE"
        elif state == "ANSWER":
            answer = llm(ANSWER.format(q=question, ev=_fmt(evidence.values())))
            state = "DONE"
    return {"answer": answer, "rounds": rounds, "evidence": list(evidence.values()),
            "sources": {c["id"]: c["url"] for c in evidence.values()}}
