from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP

# Maps file extensions to LangChain's language-aware splitters
LANG_MAP = {
    ".py":   Language.PYTHON,
    ".js":   Language.JS,
    ".ts":   Language.JS,
    ".jsx":  Language.JS,
    ".tsx":  Language.JS,
    ".md":   Language.MARKDOWN,
    ".html": Language.HTML,
}

def get_splitter(ext: str) -> RecursiveCharacterTextSplitter:
    """
    Return a language-aware splitter if we know the language,
    otherwise return a generic one.
    """
    if ext in LANG_MAP:
        return RecursiveCharacterTextSplitter.from_language(
            language=LANG_MAP[ext],
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    # Generic fallback for .yaml, .json, .sh etc
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

def chunk_documents(docs: list[Document]) -> list[Document]:
    all_chunks = []

    for doc in docs:
        ext      = doc.metadata.get("extension", "")
        splitter = get_splitter(ext)
        chunks   = splitter.split_documents([doc])

        # Add chunk index to each chunk's metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i

        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks