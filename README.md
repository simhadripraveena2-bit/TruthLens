# TruthLens 🔍
### AI Hallucination Detector — Gemma 4 Good Hackathon 2026

TruthLens is an open-source web application that detects hallucinations in AI-generated text. Paste any AI-generated content into the app, and TruthLens uses **Gemma 3 4B** running locally via **Ollama** to evaluate every sentence for accuracy, uncertainty, and hallucinations — with zero data leaving your machine.

> Built for the **Safety & Trust** track of the [Gemma 4 Good Hackathon](https://kaggle.com/competitions/gemma-4-good-hackathon) on Kaggle.

---

## ✨ Features

- 🔍 **Sentence-level analysis** — every sentence is individually classified
- 📊 **Trust Score (0–100)** — instant overall reliability rating
- 🟢🟡🔴 **Color-coded results** — Accurate / Uncertain / Hallucination
- 💡 **Hover tooltips** — plain-language explanation for every sentence
- 🔒 **100% local** — your text never leaves your machine
- ⚡ **Edge-optimized** — runs on consumer hardware, no GPU required

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 (Create React App) + plain CSS |
| Backend | FastAPI (Python) |
| AI Model | Gemma 3 4B via Ollama (edge deployment) |
| Model Target | Gemma 4 27B (high-accuracy environments) |
| Communication | REST API (HTTP/JSON) |

---

## 📁 Project Structure

```
TruthLens/
├── backend/
│   ├── main.py          # FastAPI app + endpoints
│   ├── analyzer.py      # Gemma hallucination analysis logic
│   ├── requirements.txt
│   └── .venv/           # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── TrustScore.jsx
│   │       ├── HighlightedText.jsx
│   │       └── ResultPanel.jsx
│   ├── package.json
│   └── public/
└── README.md
```

---

## 🚀 Setup Instructions

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://python.org/) (v3.10 or higher)
- [Ollama](https://ollama.com/download)

---

### Step 1 — Install Ollama

Download and install Ollama for your OS from:
👉 https://ollama.com/download

Verify installation:
```bash
ollama --version
```

---

### Step 2 — Pull the Gemma model

```bash
# Recommended — fast, edge-optimized (3GB)
ollama pull gemma3:4b

# Optional — highest accuracy (9.6GB, needs 16GB+ RAM)
ollama pull gemma4
```

---

### Step 3 — Verify Ollama is running

Ollama starts automatically on Windows. Verify with:
```bash
ollama list
```

You should see `gemma3:4b` in the list. If Ollama isn't running:
```bash
ollama serve
```

---

### Step 4 — Start the Backend

Open a terminal in the `backend` folder:

**Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**macOS / Linux:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

Verify it's working:
```
http://localhost:8000/
→ {"status": "TruthLens backend is running!"}

http://localhost:8000/test
→ Returns a sample analysis (tests Gemma connection)
```

---

### Step 5 — Start the Frontend

Open a **second terminal** in the `frontend` folder:

```bash
cd frontend
npm install
npm start
```

App opens automatically at: `http://localhost:3000`

---

## 🔌 API Reference

### `POST /analyze`

Analyzes AI-generated text for hallucinations.

**Request:**
```json
{
  "text": "Your AI-generated text here"
}
```

**Response:**
```json
{
  "trust_score": 65,
  "overall_verdict": "Contains some accurate facts but includes a clear hallucination.",
  "sentences": [
    {
      "text": "Einstein was born in Germany.",
      "risk_level": "green",
      "explanation": "Accurate — Einstein was born in Ulm, Germany in 1879."
    },
    {
      "text": "He invented the television.",
      "risk_level": "red",
      "explanation": "False — The television was invented by Philo Farnsworth, not Einstein."
    }
  ]
}
```

**Risk levels:**
| Value | Meaning |
|---|---|
| `green` | Accurate and verifiable |
| `yellow` | Uncertain or unverifiable |
| `red` | Hallucination or clearly false |

---

## 🧪 Example Test Inputs

**Test 1 — Einstein (clear hallucination):**
```
Albert Einstein was born in Ulm, Germany in 1879.
He won the Nobel Prize in Physics in 1921.
Einstein attended Harvard University for his PhD.
He also invented the telephone.
```

**Test 2 — Medical (high stakes):**
```
The human body contains 206 bones in adults.
Penicillin was discovered by Alexander Fleming in 1928.
Drinking bleach in small amounts can cure bacterial infections.
The human brain uses approximately 20% of the body's total energy.
```

---

## ⚙️ Configuration

### Switching models

In `backend/analyzer.py`, change the model name:

```python
# Fast, edge-optimized (recommended for demos)
"model": "gemma3:4b"

# Highest accuracy (requires 16GB+ RAM, slower)
"model": "gemma4"
```

### Timeout

For slower machines or larger models, increase the timeout:
```python
timeout=300  # seconds
```

---

## 🏗️ How It Works

```
User pastes text
      ↓
React frontend (App.js)
      ↓ POST /analyze
FastAPI backend (main.py)
      ↓
analyzer.py → Ollama API (localhost:11434)
      ↓
Gemma 3 4B processes prompt
      ↓
Returns structured JSON
      ↓
Frontend renders:
  • Trust Score gauge
  • Color-coded sentences
  • Hover tooltips with explanations
```

---

## 🐛 Troubleshooting

| Problem | Fix |
|---|---|
| `500 Internal Server Error` | Check FastAPI terminal for details. Usually Ollama timeout — increase `timeout=300` in `analyzer.py` |
| `Could not connect to backend` | Make sure FastAPI is running at `localhost:8000` |
| Ollama not responding | Run `ollama list` to verify. Restart with `ollama serve` |
| Results show 0 sentences | Open F12 → Console in browser and check for errors |
| First request very slow | Normal — model loads into RAM on first request. Subsequent requests are faster |

---

## 📝 Notes

- CORS is enabled for all origins in development
- The `/test` endpoint at `http://localhost:8000/test` tests the Gemma connection directly
- Model stays loaded in RAM for 10 minutes between requests (`keep_alive: 10m`)
- For production, restrict CORS origins and add rate limiting

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Google Gemma](https://ai.google.dev/gemma) — open model family
- [Ollama](https://ollama.com) — local model runtime
- [FastAPI](https://fastapi.tiangolo.com) — Python web framework
- [Kaggle](https://kaggle.com) — Gemma 4 Good Hackathon platform

---

*Submitted to the Gemma 4 Good Hackathon 2026 — Safety & Trust Track*