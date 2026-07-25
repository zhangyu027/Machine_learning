from __future__ import annotations

from typing import Iterable


def build_prompt(question: str, retrieved_chunks: list) -> str:
    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(
            f"[Source: {chunk['filename']} | Chunk: {chunk['chunk_index']} | Score: {chunk['score']:.3f}]\n"
            f"{chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_blocks)
    return f"""
You are a local private-document assistant.

Use only the supplied context. Do not invent facts.
If the context is insufficient, state that the answer is not found in the provided documents.
Cite every material claim using the source filename and chunk number.

Context:
{context}

Question:
{question}

Answer with citations:
""".strip()


def ask_ollama(question: str, retrieved_chunks: list, model_name: str = "llama3.2") -> str:
    import ollama
    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": build_prompt(question, retrieved_chunks)}],
    )
    return response["message"]["content"]


def stream_ollama(question: str, retrieved_chunks: list, model_name: str = "llama3.2") -> Iterable[str]:
    import ollama
    stream = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": build_prompt(question, retrieved_chunks)}],
        stream=True,
    )
    for chunk in stream:
        text = chunk.get("message", {}).get("content", "")
        if text:
            yield text
