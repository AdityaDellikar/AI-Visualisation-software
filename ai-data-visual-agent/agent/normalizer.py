from typing import Dict, List, Any

ALLOWED_CHART_TYPES = {
    "line_chart": "line",
    "line": "line",
    "bar_chart": "bar",
    "bar": "bar",
    "histogram": "histogram",
    "heatmap": "heatmap",
    "pie_chart": "pie",
    "pie": "pie",
    "map": "map",
}

DEFAULT_INTERACTIONS = ["hover", "filter"]

print("✅ LOADED NORMALIZER.PY")


# ----------------------------
# SAFE helpers
# ----------------------------
def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(str(v) for v in value).lower()
    if isinstance(value, str):
        return value.lower()
    return ""


def _pick_field(value: Any, fallback: str) -> str:
    """
    🔒 GUARANTEE x/y are strings
    """
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return fallback


# ----------------------------
# Chart type inference
# ----------------------------
def infer_chart_type(text: str) -> str:
    if not text:
        return "bar"

    t = text.lower()

    if any(k in t for k in ["line", "trend", "over time", "time series"]):
        return "line"
    if any(k in t for k in ["histogram", "distribution"]):
        return "histogram"
    if any(k in t for k in ["pie", "share", "percentage"]):
        return "pie"
    if any(k in t for k in ["map", "region", "geographic"]):
        return "map"
    if any(k in t for k in ["bar", "compare"]):
        return "bar"

    return "bar"


# ----------------------------
# Confidence scoring
# ----------------------------
def compute_confidence(chart_type: str, x, y, description: str) -> Dict:
    score = 0.5
    reasons: List[str] = []

    x_text = _as_text(x)
    y_text = _as_text(y)

    if chart_type == "line" and "date" in x_text:
        score += 0.2
        reasons.append("Time-based data aligns well with a line chart.")

    if chart_type in ("bar", "pie") and any(
        k in x_text for k in ["category", "type", "group"]
    ):
        score += 0.15
        reasons.append("Categorical comparison suits this chart type.")

    if y_text and y_text not in ("value", ""):
        score += 0.1
        reasons.append("Uses a meaningful quantitative measure.")

    score = min(score, 0.95)

    label = "High" if score >= 0.8 else "Medium" if score >= 0.6 else "Low"

    return {
        "confidence": round(score, 2),
        "confidence_label": label,
        "confidence_reason": " ".join(reasons)
        or "General-purpose visualization choice.",
    }


# ----------------------------
# Context generator
# ----------------------------
def generate_context(chart_type: str, x, y) -> List[str]:
    x_text = _as_text(x)
    y_text = _as_text(y)

    if chart_type == "line":
        return [
            f"Shows how {y_text or 'values'} change over time.",
            "Useful for identifying trends.",
        ]

    if chart_type == "bar":
        return [
            f"Compares {y_text or 'values'} across categories.",
            "Helps spot differences.",
        ]

    if chart_type == "pie":
        return [
            "Shows proportions of categories.",
            "Best for relative comparison.",
        ]

    return ["Provides a high-level overview."]


# ----------------------------
# Insights
# ----------------------------
def normalize_insights(raw: Dict) -> List[str]:
    return [
        i if isinstance(i, str) else i.get("description")
        for i in raw.get("insights", [])
        if i
    ]


# ----------------------------
# Visualizations
# ----------------------------
def normalize_visualizations(raw: Dict) -> List[Dict]:
    visuals: List[Dict] = []

    raw_visuals = raw.get("visualizations") or []

    for idx, v in enumerate(raw_visuals):
        chart_type = ALLOWED_CHART_TYPES.get(
            str(v.get("type", "")).lower(),
            infer_chart_type(v.get("type", "")),
        )

        # 🔒 GUARANTEED STRINGS
        x = _pick_field(v.get("x"), "Date")
        y = _pick_field(v.get("y"), "Value")

        confidence = compute_confidence(
            chart_type, x, y, v.get("description", "")
        )

        visuals.append(
            {
                "id": f"v{idx + 1}",
                "type": chart_type,
                "title": v.get("title", ""),
                "description": v.get("description", ""),
                "x": x,
                "y": y,
                "color": v.get("color"),
                "aggregation": v.get("aggregation", "none"),
                "interactions": v.get(
                    "interactions", DEFAULT_INTERACTIONS
                ),
                "confidence": confidence["confidence"],
                "confidence_label": confidence["confidence_label"],
                "confidence_reason": confidence["confidence_reason"],
                "context": generate_context(chart_type, x, y),
            }
        )

    return visuals


# ----------------------------
# Final output
# ----------------------------
def normalize_agent_output(raw: Dict) -> Dict:
    return {
        "insights": normalize_insights(raw),
        "visualizations": normalize_visualizations(raw),
    }