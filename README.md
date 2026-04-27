# 🤖 AI PDF Chatbot

An AI-powered chatbot that allows users to upload PDF documents and ask questions based on their content. The system uses NLP, embeddings, and vector search to provide accurate answers from the uploaded document.

---

## 📌 Features

* 📄 Upload and process PDF documents
* 🔍 Extract text using PyPDF
* ✂️ Split text into meaningful chunks
* 🧠 Generate embeddings using Sentence Transformers
* ⚡ Fast similarity search using FAISS
* 🤖 Ask questions and get context-based answers
* 🚀 Backend powered by FastAPI

---

## 🛠️ Technologies Used

* Python
* FastAPI
* LangChain
* FAISS (Vector Database)
* Sentence Transformers
* PyPDF
* GROQ API (LLM)

---

## 📂 Project Structure

```
AI-PDF-Chatbot/
│── main.py
│── requirements.txt
│── faiss_index.index
│── chunks.pkl
│── ui/
│     └── pdfchatbot.py
```

---

## 🚀 How It Works

1. Upload a PDF document
2. Extract text from the PDF
3. Split text into smaller chunks
4. Convert chunks into embeddings
5. Store embeddings in FAISS index
6. User asks a question
7. Relevant chunks are retrieved
8. LLM generates the final answer

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/AI-PDF-Chatbot.git
cd AI-PDF-Chatbot
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Create `.env` file

```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the backend server

```
uvicorn main:app --reload
```

### 5. Run UI (if required)

```
python ui/pdfchatbot.py
```

---


## 🔒 Security Note

The `.env` file is not included in this repository to keep API keys secure.

---


