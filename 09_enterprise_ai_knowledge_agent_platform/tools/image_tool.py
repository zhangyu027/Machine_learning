from pathlib import Path
from typing import List, Dict


def load_image_notes(input_dir: str = "data/images") -> List[Dict]:
    """
    Lightweight image-note loader.

    Add .txt sidecar files describing image contents.
    This demonstrates PDF + image understanding workflow without requiring OCR setup.
    """
    input_path = Path(input_dir)
    notes = []

    for txt in sorted(input_path.glob("*.txt")):
        image_stem = txt.stem
        image_candidates = list(input_path.glob(image_stem + ".*"))
        image_files = [p for p in image_candidates if p.suffix.lower() in [".png", ".jpg", ".jpeg"]]

        notes.append({
            "filename": txt.name,
            "source": str(txt),
            "image_file": str(image_files[0]) if image_files else None,
            "text": txt.read_text(encoding="utf-8", errors="ignore"),
            "modality": "image_note",
            "chunk_index": 0,
        })

    return notes
