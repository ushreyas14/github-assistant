import sys
from pathlib import Path

# Add project root to sys.path so ingestion/, chain/, vectorstore/ are importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from ingestion.cloner           import clone_or_pull
from ingestion.loader           import load_repo_documents
from ingestion.chunker          import chunk_documents
from vectorstore.pinecone_store import ingest_to_pinecone, load_vectorstore
from chain.rag_chain            import build_rag_chain

st.set_page_config(page_title="GitHub Repo Assistant", page_icon="🤖")
st.title("🤖 GitHub Repo Assistant")
st.caption("Powered by Groq · LangChain · Pinecone")

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.header("📦 Load a Repository")
    repo_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/owner/repo"
    )

    col1, col2 = st.columns(2)
    with col1:
        ingest_btn = st.button("🚀 Ingest", use_container_width=True)
    with col2:
        load_btn = st.button("📂 Load", use_container_width=True)

    # Ingest fresh repo
    if ingest_btn:
        if not repo_url:
            st.error("Please enter a GitHub URL")
        else:
            with st.status("Processing...", expanded=True) as status:
                st.write("Cloning repo...")
                path, name = clone_or_pull(repo_url)

                st.write("Loading files...")
                docs = load_repo_documents(path)

                st.write(f"Chunking {len(docs)} files...")
                chunks = chunk_documents(docs)

                st.write(f"Uploading {len(chunks)} chunks to Pinecone...")
                ingest_to_pinecone(chunks, name)

                status.update(label="✅ Ready!", state="complete")

            st.session_state["repo_name"] = name
            st.session_state["messages"]  = []
            st.session_state["chain"]     = None

    # Load already ingested repo
    if load_btn:
        if not repo_url:
            st.error("Please enter a GitHub URL")
        else:
            name = repo_url.rstrip("/").split("/")[-1]
            st.session_state["repo_name"] = name
            st.session_state["messages"]  = []
            st.session_state["chain"]     = None
            st.success(f"Loaded: {name}")

    if "repo_name" in st.session_state:
        st.divider()
        st.success(f"Active: `{st.session_state['repo_name']}`")

        if st.button("🗑️ Clear Chat"):
            st.session_state["messages"] = []
            st.rerun()

# ── Build chain lazily ─────────────────────────────────────
if "repo_name" in st.session_state and st.session_state.get("chain") is None:
    with st.spinner("Connecting to Pinecone..."):
        vs    = load_vectorstore(st.session_state["repo_name"])
        chain, retriever = build_rag_chain(vs)
        st.session_state["chain"]     = chain
        st.session_state["retriever"] = retriever

# ── Chat interface ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "repo_name" not in st.session_state:
    st.info("👈 Enter a GitHub URL and click Ingest or Load")
    st.stop()

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input(f"Ask about {st.session_state.get('repo_name', 'the repo')}..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get sources
    sources = st.session_state["retriever"].invoke(prompt)

    # Stream response
    with st.chat_message("assistant"):
        response = st.write_stream(
            st.session_state["chain"].stream(prompt)
        )

    st.session_state["messages"].append({
        "role": "assistant",
        "content": response
    })

    # Show sources
    with st.expander(f"📎 {len(sources)} source chunks"):
        for i, doc in enumerate(sources, 1):
            src  = doc.metadata.get("source", "unknown")
            ext  = doc.metadata.get("extension", "").lstrip(".")
            st.markdown(f"**[{i}] `{src}`**")
            st.code(doc.page_content[:400] + "...", language=ext)