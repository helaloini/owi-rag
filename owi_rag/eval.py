"""python -m owi_rag.eval questions.jsonl [--faith]

questions.jsonl: one {"question": ..., "gold_urls": [...]} per line.
Metrics are computed on distinct document URLs. The agentic ranking is the order in which the
agent first retrieved each URL (round by round, query by query).
"""
import json
import math
import re
import sys

K = 10


def urls(chunks):
    return list(dict.fromkeys(c["url"] for c in chunks))


def recall(ranked, gold, k=K):
    return len(set(ranked[:k]) & gold) / len(gold)


def ndcg(ranked, gold, k=K):
    dcg = sum(1 / math.log2(i + 2) for i, u in enumerate(ranked[:k]) if u in gold)
    return dcg / sum(1 / math.log2(i + 2) for i in range(min(len(gold), k)))


JUDGE = """Passage:
{p}

Sentence: {s}

Does the passage support the sentence? Answer only yes or no."""


def faithfulness(result, llm):
    """Share of answer sentences supported by the chunks they cite (uncited = unsupported)."""
    by_id = {c["id"]: c["text"] for c in result["evidence"]}
    judged = []
    # citations follow the period ("... immutable. [12-3]"), so keep them with the sentence before
    # shortcut: a "]" mid-sentence (e.g. "a[0] is") also splits, fine for prose answers
    for s in filter(None, (x.strip() for x in re.split(r"(?<=[.!?\]])\s+(?!\[)", result["answer"]))):
        passage = "\n\n".join(by_id[i] for i in re.findall(r"\[([^\]]+)\]", s) if i in by_id)
        ok = bool(passage) and llm(JUDGE.format(p=passage, s=s)).strip().lower().startswith("yes")
        judged.append({"sentence": s, "supported": ok})
    return judged


def main(path, faith=False):
    from .agent import ask
    from .llm import JUDGE_MODEL, chat, judge
    from .retrieve import Retriever

    r = Retriever()
    with open(path, encoding="utf-8") as f:
        qs = [json.loads(line) for line in f if line.strip()]
    scores = {m: ([], []) for m in ("bm25", "dense", "hybrid", "hybrid+agentic")}
    judgments = []
    for q in qs:
        gold = set(q["gold_urls"])
        runs = {m: urls(r.search(m, q["question"], 50)) for m in ("bm25", "dense", "hybrid")}
        res = ask(q["question"], r, chat)
        runs["hybrid+agentic"] = urls(res["evidence"])
        for m, ranked in runs.items():
            scores[m][0].append(recall(ranked, gold))
            scores[m][1].append(ndcg(ranked, gold))
        if faith:
            judgments.append({"question": q["question"], "sentences": faithfulness(res, judge)})
    print(f"| method | Recall@{K} | nDCG@{K} |\n|---|---|---|")
    for m, (rec, nd) in scores.items():
        print(f"| {m} | {sum(rec) / len(qs):.3f} | {sum(nd) / len(qs):.3f} |")
    if faith:
        flat = [s for j in judgments for s in j["sentences"]]
        print(f"\ncitation faithfulness (LLM judge {JUDGE_MODEL}): "
              f"{sum(s['supported'] for s in flat) / len(flat):.3f} over {len(flat)} sentences")
        with open("faithfulness.json", "w", encoding="utf-8") as f:
            json.dump(judgments, f, indent=1)  # check 20 of these by hand


if __name__ == "__main__":
    main(sys.argv[1], "--faith" in sys.argv)
