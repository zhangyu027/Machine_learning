import argparse

from rag.vector_store import search_index
from rag.ollama_client import ask_ollama


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--index-dir", default="vector_store")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--model", default="llama3.2")
    args = parser.parse_args()

    results = search_index(args.question, args.index_dir, top_k=args.top_k)

    print("\nTop Retrieved Sources:")
    for item in results:
        print(f"{item['rank']}. {item['filename']} | chunk {item['chunk_index']} | score={item['score']:.3f}")

    answer = ask_ollama(args.question, results, model_name=args.model)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
