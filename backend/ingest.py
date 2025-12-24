import fitz  # PyMuPDF
from pathlib import Path


def load_policy(file_path: str) -> str:
    """
    Load policy from PDF or TXT and return clean text.
    """
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        return _load_pdf(path)
    elif path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError("Unsupported file format")


def _load_pdf(path: Path) -> str:
    text = []
    doc = fitz.open(path)

    for page in doc:
        page_text = page.get_text().strip()
        if page_text:
            text.append(page_text)

    return "\n".join(text)
