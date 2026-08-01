def citation_confidence(evidence: list[dict]) -> dict:
    if not evidence: return {"score":0.0,"label":"low","reason":"No evidence retrieved"}
    scores=[max(0.0,float(e.get("score",0))) for e in evidence]
    avg=sum(scores)/len(scores); sources=len({e.get("filename") for e in evidence})
    value=min(1.0,0.7*avg+0.1*min(sources,3))
    return {"score":round(value,3),"label":"high" if value>=.7 else "medium" if value>=.45 else "low","reason":f"avg_score={avg:.3f}; sources={sources}"}
def grounding_risk_check(answer: str,evidence:list[dict]) -> dict:
    flags=[]
    if not evidence: flags.append("No evidence retrieved")
    if evidence and not any(str(e.get("filename","")) in answer for e in evidence): flags.append("No explicit source filename appears in answer")
    if any(t in answer.lower() for t in ("guarantee","definitely","always","never proves")): flags.append("Overclaiming language")
    return {"risk_level":"low" if not flags else "medium" if len(flags)==1 else "high","flags":flags,"method":"rule_based_grounding_risk_heuristic"}
