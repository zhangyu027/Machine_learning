from agents.orchestrator import answer_question

if __name__ == "__main__":
    question = "Which portfolio projects have the highest priority and why?"
    result = answer_question(question, use_ollama=False)

    print("Route:", result["route"])
    print("Answer:")
    print(result["answer"])
    print("Confidence:", result["confidence"])
    print("Hallucination risk:", result["hallucination"])
