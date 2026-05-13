import ollama


def build_prompt(question: str, retrieved_chunks: list) -> str:
    context_blocks = []

    for chunk in retrieved_chunks:
        context_blocks.append(
            f"[Source: {chunk['filename']} | Chunk: {chunk['chunk_index']} | Score: {chunk['score']:.3f}]\n"
            f"{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""
You are a local private-document assistant.

Answer the user's question using only the context below.
If the context does not contain enough information, say that the answer is not found in the provided documents.
Always cite the source filename and chunk number.

Context:
{context}

Question:
{question}

Answer with citations:
"""
    return prompt.strip()


def ask_ollama(question: str, retrieved_chunks: list, model_name: str = "llama3.2") -> str:
    prompt = build_prompt(question, retrieved_chunks)

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response["message"]["content"]
