import { useState } from "react";
import ResultPanel from "./components/ResultPanel";
import "./index.css";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      console.log("STATUS:", res.status); // ← ADD
      const data = await res.json();
      console.log("FULL RESPONSE:", JSON.stringify(data)); // ← ADD

      if (res.ok) {
        setResult(data);
      } else {
        setError("Backend error: " + (data.detail || "Unknown error"));
      }

    } catch (err) {
      console.log("FETCH ERROR:", err.message); // ← ADD
      setError("Could not connect to backend. Make sure FastAPI is running.");
    }
    setLoading(false);
  };

  const wordCount = text.split(/\s+/).filter(Boolean).length;

  return (
    <div>
      {/* HEADER */}
      <header className="header">
        <div className="header-inner">
          <div className="header-logo">
            <span>🔍</span>
            <div>
              <h1>TruthLens</h1>
              <p>AI Hallucination Detector — Powered by Gemma 4</p>
            </div>
          </div>
          <div className="badge-row">
            {["Gemma 4", "Runs Locally", "Privacy First", "Safety & Trust"].map(b => (
              <span key={b} className="badge">{b}</span>
            ))}
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="main">

        {/* Input Card */}
        <div className="card">
          <div className="card-header">
            <h2>Paste AI-Generated Text</h2>
          </div>
          <div className="card-body">
            <textarea
              placeholder="Paste any AI-generated text here — articles, summaries, research papers, chatbot responses..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <div className="input-footer">
              <span className="word-count">
                {text.length > 0 ? `${wordCount} words` : ""}
              </span>
              <button
                className="btn-analyze"
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
              >
                {loading ? (
                  <><div className="spinner" /> Analyzing...</>
                ) : (
                  <>🔍 Analyze Text</>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && <div className="error-box">⚠️ {error}</div>}

        {/* Results */}
        {result && <ResultPanel result={result} />}

      </main>

      <footer>
        TruthLens · Built with Gemma 4 + Ollama · Gemma 4 Good Hackathon 2026
      </footer>
    </div>
  );
}