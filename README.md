# Research Paper Simplifier

An AI-powered web application that helps students and researchers quickly understand academic research papers. Users can upload a research paper in PDF format, and the system automatically generates a simplified summary, identifies key contributions, explains the methodology in easy-to-understand language, suggests future research directions, generates viva questions, and provides a chatbot for asking questions about the uploaded paper.

---

## &#x20;Features

### PDF Upload & Text Extraction

* Upload research papers in PDF format
* Extract text automatically from all pages
* Clean and preprocess extracted content

### Research Paper Simplification

* Generate a concise summary
* Identify key contributions
* Explain methodology in simple language
* Suggest future scope and research opportunities
* Generate viva questions with answers

### Research Paper Chatbot

* Ask questions about the uploaded paper
* Context-aware responses based on paper content
* Prevents hallucinations by restricting answers to the uploaded document
* Maintains chat history during the session

---

## Tech Stack

| Component              | Technology           |
| ---------------------- | -------------------- |
| Frontend               | Streamlit            |
| Backend                | Python               |
| LLM API                | Groq                 |
| Model                  | Llama 3.1 8B Instant |
| PDF Processing         | pdfplumber           |
| Environment Management | python-dotenv        |
| Version Control        | Git & GitHub         |

---

## Project Structure

```text
research-paper-simplifier/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── modules/
│   ├── pdf_extractor.py
│   ├── groq_client.py
│   ├── simplifier.py
│   └── chatbot.py
│
└── assets/
    └── screenshots/
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/research-paper-simplifier.git

cd research-paper-simplifier
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Groq API Setup

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

Get your API key from:

https://console.groq.com

##

---

## 📋 Workflow

1. Upload a research paper PDF.
2. Extract and preprocess paper text.
3. Generate:

   * Summary
   * Key Contributions
   * Methodology Explanation
   * Future Scope
   * Viva Questions
4. Ask questions using the chatbot.
5. Receive context-aware responses based on the uploaded paper.

---

## 🎯 Use Cases

* Literature Review
* Research Paper Analysis
* Student Project Work
* Seminar Preparation
* Viva Preparation
* Academic Learning
* Quick Understanding of Complex Research Papers

---

## 🔮 Future Enhancements

* RAG with FAISS or ChromaDB
* Multi-Paper Comparison
* Citation Extraction
* Research Trend Analysis
* Research Paper Recommendation System
* Export Results as PDF
* Voice-Based Research Assistant
* Multi-Language Support

---

## 📸 Screenshots

---

##
