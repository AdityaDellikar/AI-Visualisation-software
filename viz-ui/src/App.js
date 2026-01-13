import React, { useState } from "react";
import VegaChart from "./components/VegaChart";
import ExcelUploader from "./components/ExcelUploader";

/**
 * ✅ Production-safe API base
 * - Local dev → http://127.0.0.1:8000
 * - Vercel → uses REACT_APP_API_BASE_URL
 */
const API_BASE =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [charts, setCharts] = useState([]);
  const [insights, setInsights] = useState([]);
  const [dataRows, setDataRows] = useState([]);
  const [explanation, setExplanation] = useState("");

  const [isExplaining, setIsExplaining] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  /* -----------------------------
     Analyze lifecycle
  ------------------------------ */
  const handleAnalyzeStart = () => {
    setIsAnalyzing(true);
    setCharts([]);
    setInsights([]);
    setDataRows([]);
    setExplanation("");
  };

  const handleResult = (result) => {
    setCharts(result.charts || []);
    setInsights(result.insights || []);
    setDataRows(result.data || []);
    setIsAnalyzing(false);
  };

  const handleAnalyzeError = () => {
    setIsAnalyzing(false);
    alert("❌ Failed to analyze dataset");
  };

  /* -----------------------------
     Chart explanation
  ------------------------------ */
  const handleChartClick = async (value, spec) => {
    try {
      setIsExplaining(true);
      setExplanation("");

      const res = await fetch(`${API_BASE}/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chart_description: spec.description,
          selected_value: value,
        }),
      });

      if (!res.ok) {
        throw new Error(`Explain failed: ${res.status}`);
      }

      const json = await res.json();
      setExplanation(json.explanation || "");
    } catch (err) {
      console.error("Explain failed", err);
      setExplanation("⚠️ Failed to generate explanation.");
    } finally {
      setIsExplaining(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>AI-Generated Visualizations</h1>

      {/* Upload */}
      <ExcelUploader
        onStart={handleAnalyzeStart}
        onResult={handleResult}
        onError={handleAnalyzeError}
      />

      {/* Insights */}
      {insights.length > 0 && (
        <div style={{ marginBottom: "30px" }}>
          <h2>Key Insights</h2>
          <ul>
            {insights.map((insight, idx) => (
              <li key={idx}>{insight}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Charts */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
          gap: "30px",
        }}
      >
        {charts.map((spec, index) => (
          <VegaChart
            key={spec.id || index}
            spec={{
              ...spec,
              data: { values: dataRows }, // ✅ inject data safely
            }}
            onPointClick={(value) => handleChartClick(value, spec)}
          />
        ))}
      </div>

      {/* Explanation Panel */}
      {(isExplaining || explanation) && (
        <div
          style={{
            marginTop: "40px",
            padding: "20px",
            border: "1px solid #ddd",
            background: "#fafafa",
            borderRadius: "8px",
          }}
        >
          <h3>AI Explanation</h3>
          {isExplaining ? (
            <p style={{ color: "#666" }}>
              ⏳ Analyzing selected data point…
            </p>
          ) : (
            <p style={{ whiteSpace: "pre-line" }}>{explanation}</p>
          )}
        </div>
      )}

      {/* 🌍 GLOBAL ANALYZE LOADER */}
      {isAnalyzing && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(255,255,255,0.9)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
          }}
        >
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: "20px", fontWeight: 600 }}>
              🤖 Analyzing your dataset
            </div>
            <div style={{ marginTop: "10px", color: "#555" }}>
              Generating insights & charts…
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;