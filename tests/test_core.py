from owi_rag.agent import ask
from owi_rag.chunk import chunk
from owi_rag.eval import faithfulness, ndcg, recall, urls
from owi_rag.retrieve import rrf


def test_chunk_overlaps_and_covers():
    words = [str(i) for i in range(500)]
    cs = chunk(" ".join(words), size=100, overlap=20)
    assert cs[0].split()[-20:] == cs[1].split()[:20]
    assert cs[-1].split()[-1] == "499"
    assert chunk("") == []


def test_rrf_prefers_docs_ranked_by_both():
    assert set(rrf([["a", "b", "c"], ["c", "b", "d"]])[:2]) == {"b", "c"}


def test_metrics():
    assert recall(["x", "g1", "y"], {"g1", "g2"}) == 0.5
    assert ndcg(["g1", "g2"], {"g1", "g2"}) == 1.0
    assert ndcg(["x"], {"g1"}) == 0


class FakeRetriever:
    def __init__(self):
        self.calls = []

    def search(self, mode, q, k):
        self.calls.append(q)
        return [{"id": f"{len(self.calls)}-0", "url": "http://a.org/x", "text": "sky is blue"}]


def test_agent_reformulates_once_then_answers():
    replies = iter(['{"queries": ["q1"]}', '{"enough": false, "queries": ["q2"]}',
                    '{"enough": true}', "The sky is blue [1-0]."])
    r = FakeRetriever()
    out = ask("why?", r, lambda _: next(replies))
    assert r.calls == ["q1", "q2"] and out["rounds"] == 2
    assert out["sources"] == {"1-0": "http://a.org/x", "2-0": "http://a.org/x"}


def test_agent_stops_at_max_rounds():
    r = FakeRetriever()
    def llm(p):
        return '{"enough": false, "queries": ["more"]}' if "Is the evidence" in p else "done"

    assert ask("q", r, llm, max_rounds=3)["rounds"] == 3

def test_faithfulness_counts_uncited_as_unsupported():
    res = {"answer": "Sky is blue [a]. Grass is red.", "evidence": [{"id": "a", "url": "u", "text": "t"}]}
    assert [s["supported"] for s in faithfulness(res, lambda _: "yes")] == [True, False]
    assert urls([{"url": "u"}, {"url": "u"}, {"url": "v"}]) == ["u", "v"]


def test_faithfulness_keeps_citation_after_period():
    res = {"answer": "Sky is blue. [a] [b] Grass is green. [a]",
           "evidence": [{"id": "a", "url": "u", "text": "t"}]}
    sents = faithfulness(res, lambda _: "yes")
    assert [s["sentence"] for s in sents] == ["Sky is blue. [a] [b]", "Grass is green. [a]"]
    assert all(s["supported"] for s in sents)
