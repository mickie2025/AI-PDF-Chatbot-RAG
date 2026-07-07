# 🤖 AI PDF Chatbot using RAG

An AI-powered PDF Chatbot built using **Python, Streamlit, LangChain, FAISS, and Google Gemini**. This application allows users to upload any PDF document and ask questions in natural language. The chatbot retrieves relevant information from the uploaded PDF using Retrieval-Augmented Generation (RAG) and generates accurate responses with Google Gemini.

---

## 🚀 Features

- 📄 Upload any PDF document
- 💬 Ask questions in natural language
- 🔍 Semantic search using FAISS Vector Database
- 🧠 Google Gemini Embedding Model
- 🤖 Google Gemini 2.5 Flash for response generation
- 📚 Displays retrieved context chunks
- 💾 Maintains chat history during the session
- ⚡ Fast and interactive Streamlit interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- FAISS Vector Store
- PyPDFLoader
- RecursiveCharacterTextSplitter
- python-dotenv

---

## 📂 Project Structure

```
AI-PDF-Chatbot-RAG/
│
├── app.py
├── model.py
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mickie2025/AI-PDF-Chatbot-RAG.git

cd AI-PDF-Chatbot-RAG
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

Get your API Key from Google AI Studio.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📸 Screenshots

### Home Page
<img width="1920" height="1080" alt="{27914992-6A46-486E-95F6-D30D4AB449C0}" src="https://github.com/user-attachments/assets/5fea35ae-a140-4871-aa18-9d0081eeb034" />



### Chat Interface

> Add a screenshot here.

### Retrieved Context

> Add a screenshot here.

---

## 🔄 Workflow

1. Upload a PDF document.
2. Extract text from the PDF.
3. Split text into chunks.
4. Generate embeddings using Google Gemini.
5. Store embeddings in FAISS.
6. Retrieve relevant chunks based on the user's question.
7. Generate the final answer using Gemini 2.5 Flash.
8. Display the answer and retrieved context.

---

## 📈 Future Improvements

- Support multiple PDF uploads
- Conversation memory across sessions
- Source page citation
- Export chat history
- Authentication system
- Deploy using Streamlit Cloud

---

## 👨‍💻 Author

**Vikram M**

B.Tech – Artificial Intelligence and Data Science

GitHub: https://github.com/mickie2025

LinkedIn: www.linkedin.com/in/vikram004

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
