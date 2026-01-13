# CodeLearn AI

An AI-powered data structures learning platform that combines LLaMA-3 language model with RAG (Retrieval-Augmented Generation) to provide interactive visualizations and personalized tutoring for data structures and algorithms.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [RAG Workflow](#rag-workflow)
- [API Endpoints](#api-endpoints)
- [Future Fine-Tuning Plan](#future-fine-tuning-plan)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Project Overview

CodeLearn AI is an educational platform designed to help learners understand data structures through:

- **Interactive Visualizations**: Real-time, interactive HTML/CSS/JavaScript visualizers for data structures (Stack, Queue, Linked List, etc.)
- **AI-Powered Tutoring**: LLaMA-3 model provides explanations, code examples, and complexity analysis
- **RAG-Enhanced Responses**: Retrieval-Augmented Generation ensures accurate, context-aware responses from a knowledge base
- **Dual Chat Modes**: 
  - **General Mode**: General coding assistance
  - **DS Mode**: Specialized data structure tutoring with complexity analysis

## 🏗️ Architecture

### System Components

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   FastAPI    │────────▶│   LLaMA-3   │
│  (React +   │         │   Backend    │         │   Model     │
│   TypeScript)│         │              │         │             │
└─────────────┘         └──────┬───────┘         └─────────────┘
                                │
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼──────┐      ┌────────▼────────┐
            │   ChromaDB   │      │  RAG Pipeline   │
            │  (Vector DB) │      │  (LangChain)    │
            └──────────────┘      └─────────────────┘
```

### Backend Architecture

1. **API Layer** (`app/api/`)
   - `chat.py`: Chat endpoint with dual modes (general/DS)
   - `rag.py`: RAG query endpoint for visualizer retrieval

2. **Core Services** (`app/core/`)
   - `llm.py`: LLaMA-3 model loader with lazy loading
   - `rag_pipeline.py`: LangChain-based RAG pipeline for document retrieval

3. **Data Layer** (`app/db/`)
   - `chroma_store.py`: ChromaDB integration with SentenceTransformer embeddings
   - `seed_data.py`: Script to seed visualizers into the knowledge base

4. **Utilities** (`app/utils/`)
   - `prompts.py`: System prompts for different AI roles

### Frontend Architecture

- **React + TypeScript**: Modern UI framework
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Components**:
  - `Sidebar.tsx`: Navigation component
  - `DSWorkspace.tsx`: Data structure workspace
  - `Visualizer.tsx`: Interactive visualizer renderer
  - `Chat.tsx` / `DSChat.tsx`: Chat interfaces

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** and npm
- **Git**

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend` directory:
   ```env
   # LLM Configuration
   LLM_MODEL_PATH=meta-llama/Meta-Llama-3-8B
   LLM_DEVICE_MAP=auto
   LLM_TORCH_DTYPE=float16
   LLM_MAX_LENGTH=512
   LLM_TEMPERATURE=0.7
   LLM_TOP_P=0.9
   LLM_DO_SAMPLE=true
   
   # ChromaDB Configuration
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   CHROMA_COLLECTION_NAME=codelearn_documents
   CHROMA_EMBEDDING_MODEL=all-MiniLM-L6-v2
   ```

5. **Seed the database with visualizers:**
   ```bash
   python -m app.db.seed_data
   ```

6. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at:
   - API: `http://localhost:8000`
   - Interactive Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173` (or the port shown in terminal)

4. **Build for production:**
   ```bash
   npm run build
   ```

## 🔄 RAG Workflow

The RAG (Retrieval-Augmented Generation) workflow enables context-aware responses by combining retrieval with generation:

### 1. **Document Storage**
- Interactive visualizer code (HTML/CSS/JS) is stored in ChromaDB
- Each document includes:
  - Full visualizer code
  - Metadata (name, description, data structure type)
  - Embeddings generated using SentenceTransformer

### 2. **Query Processing**
```
User Query: "Show me a stack visualizer"
    ↓
Embedding Generation (SentenceTransformer)
    ↓
Similarity Search in ChromaDB
    ↓
Retrieve Top-K Documents
    ↓
Return: Description + Raw Visualizer Code
```

### 3. **Retrieval Process**

1. **Query Embedding**: User query is embedded using the same SentenceTransformer model
2. **Vector Search**: ChromaDB performs cosine similarity search
3. **Metadata Filtering**: Optional filtering by data structure type
4. **Result Return**: Returns raw HTML/CSS/JS code without modification

### 4. **Integration Points**

- **RAG Endpoint** (`/api/rag/query`): Direct visualizer retrieval
- **Chat Endpoint** (`/api/chat/`): Can be enhanced to use RAG for context

## 📡 API Endpoints

### Chat Endpoint

**POST** `/api/chat/`

Request:
```json
{
  "message": "Explain how a stack works",
  "mode": "ds"
}
```

Response:
```json
{
  "success": true,
  "response": "A stack is a linear data structure...",
  "mode": "ds"
}
```

### RAG Query Endpoint

**POST** `/api/rag/query`

Request:
```json
{
  "data_structure_name": "Stack"
}
```

Response:
```json
{
  "success": true,
  "name": "Stack",
  "description": "Interactive Stack visualizer...",
  "visualizer_code": "<!DOCTYPE html>...",
  "metadata": {...}
}
```

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "service": "codelearn-ai"
}
```

## 🎯 Future Fine-Tuning Plan for LLaMA-3

### Phase 1: Data Collection & Preparation

1. **Dataset Creation**
   - Collect high-quality Q&A pairs for data structures
   - Include code examples, complexity explanations, and visual descriptions
   - Target: 10,000+ examples covering all major data structures

2. **Data Formatting**
   - Convert to instruction-following format
   - Include system prompts for different modes (general/DS)
   - Add metadata tags (topic, difficulty, operation type)

### Phase 2: Fine-Tuning Strategy

1. **Base Model Selection**
   - Start with `meta-llama/Meta-Llama-3-8B-Instruct`
   - Consider smaller variants for faster iteration

2. **Training Approach**
   - **LoRA (Low-Rank Adaptation)**: Efficient fine-tuning with reduced parameters
   - **QLoRA**: Quantized LoRA for memory efficiency
   - **Full Fine-Tuning**: For final model if resources allow

3. **Training Configuration**
   ```python
   {
     "learning_rate": 2e-4,
     "batch_size": 4,
     "gradient_accumulation_steps": 8,
     "num_epochs": 3,
     "warmup_steps": 100,
     "max_length": 2048
   }
   ```

### Phase 3: Specialized Models

1. **Mode-Specific Models**
   - **General Coding Model**: Fine-tuned on general programming questions
   - **DS Tutor Model**: Specialized for data structure explanations with complexity analysis

2. **Domain-Specific Fine-Tuning**
   - Stack/Queue operations
   - Tree traversal algorithms
   - Graph algorithms
   - Complexity analysis patterns

### Phase 4: Evaluation & Iteration

1. **Evaluation Metrics**
   - **Accuracy**: Correctness of explanations
   - **Code Quality**: Syntactic correctness and best practices
   - **Complexity Analysis**: Correctness of Big O notation
   - **User Satisfaction**: Feedback-based metrics

2. **A/B Testing**
   - Compare fine-tuned vs. base model
   - Measure response quality and user engagement

3. **Continuous Improvement**
   - Collect user feedback
   - Retrain with new data
   - Version control for model iterations

### Phase 5: Deployment Strategy

1. **Model Serving**
   - Use HuggingFace Inference API or custom serving
   - Implement model versioning
   - A/B testing infrastructure

2. **Monitoring**
   - Track response times
   - Monitor token usage
   - Error rate tracking

3. **Optimization**
   - Model quantization for faster inference
   - Caching frequently asked questions
   - Batch processing for multiple queries

### Implementation Timeline

- **Month 1-2**: Data collection and preparation
- **Month 3**: Initial fine-tuning experiments
- **Month 4**: Evaluation and refinement
- **Month 5-6**: Specialized model development
- **Month 7**: Production deployment
- **Ongoing**: Continuous improvement based on user feedback

## 📁 Project Structure

```
codelearn-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py          # Chat endpoint
│   │   │   └── rag.py            # RAG query endpoint
│   │   ├── core/
│   │   │   ├── llm.py            # LLaMA-3 loader
│   │   │   └── rag_pipeline.py   # RAG pipeline
│   │   ├── db/
│   │   │   ├── chroma_store.py   # ChromaDB integration
│   │   │   └── seed_data.py      # Database seeding
│   │   ├── utils/
│   │   │   └── prompts.py        # System prompts
│   │   └── main.py               # FastAPI app
│   ├── requirements.txt
│   └── .env                      # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── DSWorkspace.tsx
│   │   │   ├── Visualizer.tsx
│   │   │   ├── Chat.tsx
│   │   │   └── DSChat.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   └── LearnDS.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   └── package.json
│
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Meta AI** for LLaMA-3 model
- **HuggingFace** for transformers library
- **ChromaDB** for vector database
- **LangChain** for RAG pipeline framework

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Happy Learning! 🚀**
