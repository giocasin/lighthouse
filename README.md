# 🔦 Lighthouse

> Simplify onboarding on new codebases through AI-powered analysis and natural language Q&A.

Lighthouse clones a Git repository, analyzes its files, and lets you ask questions about the codebase in plain language. Built as a learning project to explore AI agent patterns and Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- **Git integration** — clone or update any repository automatically
- **Smart file scanning** — classifies and prioritizes files by type (source code, docs, configuration)
- **Intelligent chunking** — splits files using type-aware strategies for optimal embedding
- **Vector search** — stores embeddings in ChromaDB for fast semantic retrieval
- **Natural language Q&A** — ask anything about the codebase and get contextual answers

---

## 🏗️ Architecture

```
Git Clone/Pull → File Scanning → Chunking → Embedding → Vector Store → Agent Q&A
```

```
Lighthouse/
├── data/
│   └── vector_store/        # ChromaDB persistent storage
├── repos/                   # Cloned repositories
├── src/
│   ├── ingestion/
│   │   ├── loader.py        # Git clone/pull logic
│   │   ├── scanner.py       # File scanning and prioritization
│   │   └── chunker.py       # Type-aware text chunking
│   ├── embeddings/
│   │   └── embedder.py      # Embedding generation
│   ├── store/
│   │   └── vector_store.py  # ChromaDB interface
│   ├── agent/
│   │   ├── agent.py         # Agent logic
│   │   └── prompts.py       # System prompts and templates
│   └── utils/
│       ├── logging.conf
│       └── types.py         # Shared types and enums
└── tests/
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git

### Installation

```bash
git clone https://github.com/yourusername/lighthouse.git
cd lighthouse
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

```python
from src.ingestion.loader import clone_or_update
from src.ingestion.scanner import scan_repo
from src.ingestion.chunker import chunk_file
from pathlib import Path

# Clone a repository
clone_or_update("https://github.com/user/repo.git", "repos/my-repo")

# Scan and analyze
files = scan_repo(Path("repos/my-repo"))

# Chunk files for embedding
for file_info in files:
    chunks = chunk_file(file_info)
```

---

## 🔧 File Type Priorities

Lighthouse assigns a priority score to each file to determine processing order:

| Type | Priority | Examples |
|---|---|---|
| `DOCS` | 1.0 | `.md`, `.pdf`, `.txt` |
| `CONFIGURATION` | 0.8 | `.yaml`, `.json`, `Dockerfile` |
| `SOURCE_CODE` | 0.5 | `.py`, `.cs`, `.ts`, `.js` |
| `OTHER` | 0.1 | Everything else |

---

## 🧪 Running Tests

```bash
python -m unittest discover -s tests -v
```

Tests follow a TDD approach. Each module has corresponding tests covering edge cases (empty files, binary files, unknown extensions, etc.).

---

## 🛠️ Tech Stack

| Component | Library |
|---|---|
| Git operations | `gitpython` |
| Text splitting | `langchain-text-splitters` |
| Vector store | `chromadb` |
| Embeddings | `text-embedding-3-small` (OpenAI) |
| Agent | `langchain` |

---

## 📚 Background

This project was built as a hands-on exploration of:
- **RAG (Retrieval-Augmented Generation)** patterns
- **AI agent** design and tool use
- **LangChain** ecosystem
- **ChromaDB** for vector storage

---

## 📄 License

MIT