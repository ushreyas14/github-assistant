import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX   = os.getenv("PINECONE_INDEX_NAME", "github-rag")

# Models
GROQ_MODEL = "llama-3.3-70b-versatile"
EMBED_MODEL = "all-MiniLM-L6-v2"
EMBED_DIM   = 384

# Chunking
CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 150
TOP_K         = 8

# What files to index
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".md", ".txt",
    ".yaml", ".yml", ".json", ".html", ".sh"
}

# What folders to skip
IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__",
    ".venv", "dist", "build"
}