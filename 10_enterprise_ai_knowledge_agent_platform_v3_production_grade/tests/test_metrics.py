from enterprise_ai_agent.evaluation.metrics import recall_at_k,reciprocal_rank,route_accuracy
def test_metrics():
    assert recall_at_k(["a","b"],{"a","c"},2)==0.5
    assert reciprocal_rank(["x","a"],{"a"})==0.5
    assert route_accuracy(["a","b"],["a","c"])==0.5
