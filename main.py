from ingestion.cloner  import clone_or_pull
from ingestion.loader  import load_repo_documents
from ingestion.chunker import chunk_documents
from chain.embeddings import get_embeddings

from ingestion.cloner          import clone_or_pull
from ingestion.loader          import load_repo_documents
from ingestion.chunker         import chunk_documents
from vectorstore.pinecone_store import ingest_to_pinecone

from vectorstore.pinecone_store import load_vectorstore
from chain.rag_chain import build_rag_chain

# path, name = clone_or_pull("https://github.com/pallets/flask")
# docs   = load_repo_documents(path)
# chunks = chunk_documents(docs)

# # Inspect a chunk
# print("\n--- Sample Chunk ---")
# print(chunks[0].page_content)
# print("\nMetadata:", chunks[0].metadata)

# embeddings = get_embeddings()

# test_vector = embeddings.embed_query("Rahul is gay")

# print(f"Vector length: {len(test_vector)}")
# print(f"First 5 values: {test_vector[:5]}")

path, name = clone_or_pull("https://github.com/ushreyas14/hotel_management")
docs       = load_repo_documents(path)
chunks     = chunk_documents(docs)
vs         = ingest_to_pinecone(chunks, name)

print("Done! Chunks are now in Pinecone.")

vs = load_vectorstore("flask")
chain, retriever = build_rag_chain(vs)

question = "How does Flask handle URL routing?"

print(f"\nQ: {question}\n")
print("A: ", end="", flush=True)

for chunk in chain.stream(question):
    print(chunk, end="", flush=True)

print()