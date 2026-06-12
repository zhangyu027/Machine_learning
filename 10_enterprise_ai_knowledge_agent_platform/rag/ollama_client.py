try:
    import ollama  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    ollama = None


def build_grounded_prompt(question: str, evidence: list) -> str:
    blocks = []
    for item in evidence:
        blocks.append(
            f"[Source: {item.get('filename', 'unknown')} | Chunk: {item.get('chunk_index', 'n/a')} | Score: {item.get('score', 0):.3f}]\n"
            f"{item.get('text', '')}"
        )
    context = "\n\n---\n\n".join(blocks)

    return f"""
You are an enterprise AI knowledge agent.

Answer the question using ONLY the evidence below.
If the evidence is insufficient, say the answer is not fully supported.
Always cite source filename and chunk number when possible.

Evidence:
{context}

Question:
{question}

Answer:
""".strip()


def ask_ollama(question: str, evidence: list, model_name: str = "llama3.2") -> str:
    prompt = build_grounded_prompt(question, evidence)
    if ollama is None:
        return (
            "Ollama is not installed in this environment. Retrieved evidence summary:\n\n"
            + "\n\n".join([
                f"{item.get('filename', 'unknown')} chunk {item.get('chunk_index', 'n/a')}: {item.get('text', '')[:500]}"
                for item in evidence
            ])
        )
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
