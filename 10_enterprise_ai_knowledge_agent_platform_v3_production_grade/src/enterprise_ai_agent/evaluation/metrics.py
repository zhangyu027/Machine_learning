def recall_at_k(retrieved:list[str], relevant:set[str], k:int)->float:
    return len(set(retrieved[:k]) & relevant)/len(relevant) if relevant else 0.0
def reciprocal_rank(retrieved:list[str], relevant:set[str])->float:
    for i,item in enumerate(retrieved,1):
        if item in relevant:return 1.0/i
    return 0.0
def citation_precision(citations:list[str],supporting:set[str])->float:
    return sum(c in supporting for c in citations)/len(citations) if citations else 0.0
def route_accuracy(predicted:list[str],expected:list[str])->float:
    return sum(p==e for p,e in zip(predicted,expected))/len(expected) if expected else 0.0
