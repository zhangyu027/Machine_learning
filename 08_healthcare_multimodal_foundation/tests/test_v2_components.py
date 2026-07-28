import numpy as np
from src.healthcare_mm.models.multimodal_transformer import MultimodalFusionEncoder
from retrieval.vector_store import InMemoryVectorStore
from rag.clinical_rag import ClinicalRAG
from evaluation.multimodal_eval import recall_at_k, reciprocal_rank
from fhir.client import FHIRClient
from feedback.review import FeedbackRepository, ClinicianReview


def test_multimodal_fusion_shape():
    model = MultimodalFusionEncoder(4, 5, 3, hidden_dim=8)
    out = model.encode(np.ones((2,4)), np.ones((2,5)), np.ones((2,3)))
    assert out["fused"].shape == (2,8)
    assert np.allclose(out["modality_weights"].sum(axis=1), 1)


def test_vector_search_and_rag():
    store = InMemoryVectorStore(); store.add("Guideline/1", [1,0], "Guideline supports intervention.")
    store.add("Note/2", [0,1], "Unrelated note.")
    hits = store.search([1,0], top_k=1)
    assert hits[0].document_id == "Guideline/1"
    response = ClinicalRAG(store).answer("What supports intervention?", [1,0])
    assert response.citations == ["Guideline/1"]


def test_retrieval_metrics():
    assert recall_at_k(["a","b"], {"b"}, 2) == 1
    assert reciprocal_rank(["a","b"], {"b"}) == .5


def test_fhir_and_feedback(tmp_path):
    client = FHIRClient(); resource = client.create_risk_assessment("p1", .8, "reason", ["Observation/o1"])
    assert resource["resourceType"] == "RiskAssessment"
    repo = FeedbackRepository(str(tmp_path/"feedback.jsonl"))
    row = repo.record(ClinicianReview("pred1", "clin1", "accept"))
    assert row["decision"] == "accept"
