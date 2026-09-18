def chunk_text(text, chunk_size=500, overlap=50):
    paragraphs = text.splitlines()

    chunks = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current) + len(paragraph) + 1 <= chunk_size:
            current += paragraph + "\n"
        else:
            if current.strip():
                chunks.append(current.strip())

            current = paragraph + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks