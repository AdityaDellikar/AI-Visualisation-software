import React, { useRef, useEffect, useState } from "react";
import vegaEmbed from "vega-embed";

/* -----------------------------
   Small UI helpers
------------------------------ */
const ConfidenceBadge = ({ score, label }) => {
  let bg = "#e5e7eb";
  if (label === "High") bg = "#dcfce7";
  if (label === "Medium") bg = "#fef3c7";
  if (label === "Low") bg = "#fee2e2";

  return (
    <span
      style={{
        background: bg,
        padding: "4px 10px",
        borderRadius: "999px",
        fontSize: "12px",
        fontWeight: 600,
      }}
    >
      {score} – {label}
    </span>
  );
};

const Spinner = () => (
  <div style={{ fontSize: "13px", color: "#666" }}>⏳ Loading…</div>
);

/* -----------------------------
   Main Component
------------------------------ */
const VegaChart = ({ spec, onPointClick }) => {
  const containerRef = useRef(null);
  const [isRendering, setIsRendering] = useState(true);
  const [isExplaining, setIsExplaining] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    let view;
    setIsRendering(true);

    vegaEmbed(containerRef.current, spec, { actions: false })
      .then((result) => {
        view = result.view;
        setIsRendering(false);

        view.addEventListener("click", (event, item) => {
          if (!item || !item.datum || !onPointClick) return;

          setIsExplaining(true);

          const safeDatum = {
            ...item.datum,
            value:
              item.datum.value ??
              item.datum.count ??
              item.datum.__count ??
              null,
          };

          Promise.resolve(onPointClick(safeDatum)).finally(() =>
            setIsExplaining(false)
          );
        });
      })
      .catch((err) => {
        console.error("Vega render failed:", err);
        setIsRendering(false);
      });

    return () => {
      if (view) view.finalize();
    };
  }, [spec, onPointClick]);

  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: "10px",
        padding: "16px",
        background: "#fff",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "8px",
        }}
      >
        <p style={{ fontWeight: "600", margin: 0 }}>
          {spec.description || "Chart"}
        </p>

        {spec.confidence !== undefined && (
          <ConfidenceBadge
            score={spec.confidence}
            label={spec.confidence_label}
          />
        )}
      </div>

      {/* Context */}
      {spec.context && (
        <div style={{ fontSize: "13px", color: "#555", marginBottom: "8px" }}>
          {spec.context.slice(0, 3).map((line, idx) => (
            <div key={idx}>• {line}</div>
          ))}
        </div>
      )}

      {/* Chart container MUST ALWAYS EXIST */}
      <div style={{ position: "relative", minHeight: "240px" }}>
        {isRendering && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "rgba(255,255,255,0.8)",
              zIndex: 1,
            }}
          >
            <Spinner />
          </div>
        )}

        <div ref={containerRef} />
      </div>

      {/* Explain spinner */}
      {isExplaining && (
        <div style={{ marginTop: "8px" }}>
          <Spinner />
        </div>
      )}
    </div>
  );
};

export default VegaChart;