from typing import Literal
Route = Literal["sql_agent","image_agent","document_rag_agent"]
def route_question(question: str) -> Route:
    q=question.lower()
    if any(t in q for t in ("portfolio","highest priority","project metrics","risk level","table")): return "sql_agent"
    if any(t in q for t in ("image","diagram","architecture picture","screenshot")): return "image_agent"
    return "document_rag_agent"
