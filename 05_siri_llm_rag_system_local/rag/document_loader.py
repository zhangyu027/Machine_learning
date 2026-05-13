from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader


def load_txt_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append(f"\n[Page {i + 1}]\n{text}")
    return "\n".join(pages)


def load_documents(input_dir: str) -> List[Dict]:
    input_path = Path(input_dir)
    docs = []

    if not input_path.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_path}")

    for path in sorted(input_path.rglob("*")):
        if path.is_dir():
            continue

        suffix = path.suffix.lower()

        if suffix == ".txt":
            text = load_txt_file(path)
        elif suffix == ".pdf":
            text = load_pdf_file(path)
        else:
            continue

        if text.strip():
            docs.append({
                "source": str(path),
                "filename": path.name,
                "text": text,
            })

    return docs


def chunk_text(text: str, chunk_size: int = 900, chunk_overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def create_chunks(documents: List[Dict], chunk_size: int = 900, chunk_overlap: int = 150) -> List[Dict]:
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{doc['filename']}::chunk_{idx}",
                "source": doc["source"],
                "filename": doc["filename"],
                "chunk_index": idx,
                "text": chunk,
            })

    return all_chunks
