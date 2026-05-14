def citation_confidence(evidence: list):
    if not evidence:
        return {"confidence_score": 0.0, "confidence_label": "low", "reason": "No retrieved evidence."}

    scores = [float(item.get("score", 0)) for item in evidence]
    avg_score = sum(scores) / len(scores)
    source_count = len(set(item.get("filename", "unknown") for item in evidence))
    confidence = min(1.0, 0.65 * avg_score + 0.10 * min(source_count, 3))

    if confidence >= 0.70:
        label = "high"
    elif confidence >= 0.45:
        label = "medium"
    else:
        label = "low"

    return {
        "confidence_score": round(confidence, 3),
        "confidence_label": label,
        "reason": f"Average retrieval score={avg_score:.3f}; distinct sources={source_count}.",
    }


def hallucination_risk_check(answer: str, evidence: list):
    if not evidence:
        return {"risk_level": "high", "flags": ["No evidence retrieved."]}

    flags = []

    if "source" not in answer.lower() and "chunk" not in answer.lower() and "ollama disabled" not in answer.lower():
        flags.append("Answer may not contain explicit source citation language.")

    overclaim_terms = ["guarantee", "always", "never", "proves", "definitely"]
    if any(term in answer.lower() for term in overclaim_terms):
        flags.append("Answer may contain overclaiming language.")

    if len(answer.split()) > 220:
        flags.append("Answer is long; review for unsupported details.")

    if not flags:
        risk = "low"
    elif len(flags) == 1:
        risk = "medium"
    else:
        risk = "high"

    return {"risk_level": risk, "flags": flags}
