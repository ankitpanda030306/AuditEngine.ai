# 🛡️ AuditEngine-AI

**Autonomous Multi-Modal Infrastructure Telemetry Auditor & Governance Engine**

AuditEngine-AI combines classical machine learning, PyTorch deep learning vision backbones, vector search (RAG), and deterministic orchestration to detect infrastructure anomalies and dispatch automated mitigations.

---

## 🏗️ Architecture & Core Components

- **Classical ML (`log_analyzer.py`):** Scikit-Learn `IsolationForest` for unsupervised telemetry anomaly detection and risk scoring.
- **Deep Learning Vision (`vision_inspector.py`):** PyTorch `MobileNetV3` transfer learning backbone to classify system architecture diagrams.
- **Vector RAG (`rag_engine.py`):** Local Hugging Face `sentence-transformers/all-MiniLM-L6-v2` embeddings with ChromaDB cosine similarity search.
- **Agent Orchestrator (`agent_executor.py`):** Multi-modal telemetry evaluation and remediation dispatch.
- **Interactive UI (`app.py`):** Streamlit dashboard with real-time Plotly threat gauges and similarity charts.

---

## 🚀 Quickstart

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/auditengine-ai.git
   cd auditengine-ai