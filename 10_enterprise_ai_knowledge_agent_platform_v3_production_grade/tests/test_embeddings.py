import numpy as np
from enterprise_ai_agent.rag.embeddings import stable_hash_embedding
def test_stable_embedding():
    a=stable_hash_embedding("hello world"); b=stable_hash_embedding("hello world")
    assert np.array_equal(a,b); assert a.shape==(384,)
