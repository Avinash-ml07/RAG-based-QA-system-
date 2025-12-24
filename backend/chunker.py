def chunk_policy(text: str, max_length: int = 500):
    """
    Chunk policy text by paragraphs/sections.
    """
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_length:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
