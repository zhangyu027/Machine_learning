def route_question(question: str):
    q = question.lower()

    if any(term in q for term in ["sql", "table", "portfolio", "highest priority", "project metrics", "risk level"]):
        return "sql_agent"

    if any(term in q for term in ["image", "diagram", "architecture picture", "screenshot"]):
        return "image_agent"

    return "document_rag_agent"
