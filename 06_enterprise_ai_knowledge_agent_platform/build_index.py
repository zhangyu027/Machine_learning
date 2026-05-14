from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from rag.document_loader import load_documents, create_chunks
from rag.vector_store import build_vector_store
from tools.image_tool import load_image_notes
from tools.sql_tool import load_csv_to_sqlite


def main():
    docs = load_documents("data/documents")
    doc_chunks = create_chunks(docs)

    image_notes = load_image_notes("data/images")
    image_chunks = create_chunks(image_notes)

    all_chunks = doc_chunks + image_chunks
    build_vector_store(all_chunks, "vector_store")

    load_csv_to_sqlite(
        csv_path="data/sql/project_portfolio_metrics.csv",
        table_name="portfolio_metrics",
        db_path="data/sql/enterprise_agent.db",
    )

    print(f"Indexed chunks: {len(all_chunks)}")
    print("Vector store saved to vector_store/")
    print("SQL database saved to data/sql/enterprise_agent.db")


if __name__ == "__main__":
    main()
