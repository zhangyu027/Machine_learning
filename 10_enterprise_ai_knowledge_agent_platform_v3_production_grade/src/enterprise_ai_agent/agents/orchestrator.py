from __future__ import annotations
import time, uuid
from pathlib import Path
from .router import route_question
from enterprise_ai_agent.rag.vector_store import search
from enterprise_ai_agent.security.prompt_guard import assess_untrusted_text
from enterprise_ai_agent.tools.grounding import citation_confidence, grounding_risk_check
from enterprise_ai_agent.tools.sql_tool import run_template, select_template

def answer_question(question:str,index_dir:Path,db_path:Path,top_k:int=5)->dict:
    started=time.perf_counter(); route=route_question(question); evidence=[]; sql_template=None
    if route=="sql_agent":
        sql_template=select_template(question); df=run_template(sql_template,db_path)
        evidence=[{"filename":"project_portfolio_metrics.csv","chunk_index":"sql","score":1.0,"text":df.to_string(index=False),"modality":"sql"}]
    else:
        evidence=search(question,index_dir,top_k)
    unsafe=[e for e in evidence if not assess_untrusted_text(e.get("text","")).get("safe")]
    if not evidence:
        answer="I do not have enough evidence to answer this question."
    else:
        lines=[f"- {e['filename']} (chunk {e.get('chunk_index')}): {e.get('text','')[:280]}" for e in evidence]
        answer="Evidence-based summary:\n"+"\n".join(lines)
        if unsafe: answer+="\nSome retrieved content was flagged as untrusted and was not treated as instructions."
    return {"request_id":str(uuid.uuid4()),"route":route,"answer":answer,"citations":[e["filename"] for e in evidence],"evidence":evidence,"confidence":citation_confidence(evidence),"grounding_risk":grounding_risk_check(answer,evidence),"latency_ms":round((time.perf_counter()-started)*1000,2),"sql_template":sql_template,"index_version":evidence[0].get("index_version") if evidence else None}
