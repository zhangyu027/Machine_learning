from pathlib import Path
import argparse

from rag.document_loader import load_documents, create_chunks
from rag.vector_store import build_faiss_index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/sample_documents", help="Folder containing .txt and .pdf files.")
    parser.add_argument("--index-dir", default="vector_store", help="Folder to save FAISS index.")
    parser.add_argument("--chunk-size", type=int, default=900)
    parser.add_argument("--chunk-overlap", type=int, default=150)
    parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2")
    args = parser.parse_args()

    documents = load_documents(args.input_dir)
    print(f"Loaded documents: {len(documents)}")

    chunks = create_chunks(
        documents,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    print(f"Created chunks: {len(chunks)}")

    build_faiss_index(
        chunks,
        output_dir=args.index_dir,
        embedding_model_name=args.embedding_model,
    )

    print(f"Saved vector store to: {Path(args.index_dir).resolve()}")


if __name__ == "__main__":
    main()
