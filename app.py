from dotenv import load_dotenv
import os
import tempfile
import streamlit as st

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# -------------------------------------------------
# Streamlit Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🤖 AI PDF Chatbot using RAG")

st.markdown("""
Ask questions about any PDF using **Gemini + LangChain + FAISS**.

Upload a PDF and start chatting with it.
""")

st.divider()

# -------------------------------------------------
# Clear Chat
# -------------------------------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------------------------------
# Upload PDF
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# -------------------------------------------------
# Process PDF only once
# -------------------------------------------------
if uploaded_file is not None:

    # New PDF uploaded
    if uploaded_file.name != st.session_state.pdf_name:
        st.session_state.messages = []
        st.session_state.vector_store = None
        st.session_state.retriever = None
        st.session_state.pdf_name = uploaded_file.name

    if st.session_state.vector_store is None:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.info(f"📄 Total Pages: {len(documents)}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        st.success(f"✅ Created {len(chunks)} chunks")

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=GOOGLE_API_KEY
        )

        st.session_state.vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

        st.session_state.retriever = (
            st.session_state.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
        )

        st.success("✅ Vector Store Ready")

# -------------------------------------------------
# Display Previous Chat
# -------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# Chat Section
# -------------------------------------------------
if st.session_state.retriever is not None:

    question = st.chat_input("Ask anything about the PDF...")

    if question:

        # Display User Message
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Retrieve Relevant Chunks
        docs = st.session_state.retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        # Gemini Model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0
        )

        prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not found, reply exactly:

"I couldn't find that information in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

        with st.spinner("🤖 Gemini is thinking..."):
            response = llm.invoke(prompt)

        # Display Assistant Message
        with st.chat_message("assistant"):
            st.markdown(response.content)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.content
            }
        )

        # Retrieved Chunks
        with st.expander("📚 Retrieved Context"):
            for i, doc in enumerate(docs):
                st.markdown(f"### Chunk {i+1}")
                st.write(doc.page_content)
                st.markdown("---")

else:
    st.info("📄 Upload a PDF to start chatting.")