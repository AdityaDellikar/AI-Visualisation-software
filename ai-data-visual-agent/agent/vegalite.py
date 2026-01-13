import pandas as pd

# ----------------------------
# Helpers
# ----------------------------
def infer_field_type(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "temporal"
    if pd.api.types.is_numeric_dtype(series):
        return "quantitative"
    return "nominal"


def infer_unit(field: str | None) -> str:
    if not field:
        return "records"

    field = field.lower()
    if "age" in field:
        return "years"
    if "duration" in field:
        return "seconds"
    if "income" in field:
        return "USD"
    if "price" in field or "value" in field:
        return "value"
    return "records"


def field_is_valid(df: pd.DataFrame, field) -> bool:
    """
    🔒 HARDENED: NEVER crashes on lists / bad AI output
    """
    if not isinstance(field, str):
        return False
    if field not in df.columns:
        return False
    return df[field].notna().any()


# ----------------------------
# Confidence helpers
# ----------------------------
def compute_confidence(viz: dict, df: pd.DataFrame) -> tuple[float, list[str]]:
    reasons = []
    score = 1.0

    chart_type = viz.get("type")
    x_field = viz.get("x")
    y_field = viz.get("y")
    aggregation = viz.get("aggregation", "none")

    if x_field and field_is_valid(df, x_field):
        reasons.append("Sufficient data available on x-axis")
    else:
        score -= 0.3
        reasons.append("Limited usable data on x-axis")

    if (
        chart_type == "histogram"
        and x_field
        and field_is_valid(df, x_field)
        and pd.api.types.is_numeric_dtype(df[x_field])
    ):
        reasons.append("Histogram suits numeric distribution")

    if (
        chart_type == "line"
        and x_field
        and field_is_valid(df, x_field)
        and pd.api.types.is_datetime64_any_dtype(df[x_field])
    ):
        reasons.append("Line chart fits temporal trend")

    if (
        chart_type == "pie"
        and x_field
        and field_is_valid(df, x_field)
        and df[x_field].nunique() > 12
    ):
        score -= 0.25
        reasons.append("Too many categories for a pie chart")

    if y_field and field_is_valid(df, y_field) and aggregation != "count":
        if df[y_field].std(skipna=True) < 0.01:
            score -= 0.2
            reasons.append("Low variation in values")
        else:
            reasons.append("Strong variation in values")

    score = max(0.0, min(score, 1.0))
    return round(score, 2), reasons[:3]


def confidence_label(score: float) -> str:
    if score >= 0.85:
        return "High"
    if score >= 0.65:
        return "Medium"
    return "Low"


# ----------------------------
# Vega-Lite generator
# ----------------------------
def generate_vegalite_spec(viz: dict, df: pd.DataFrame) -> dict | None:
    chart_type = viz.get("type")
    x_field = viz.get("x")
    y_field = viz.get("y")
    aggregation = viz.get("aggregation", "none")

    # 🚫 HARD BLOCK invalid x
    if not field_is_valid(df, x_field):
        return None

    mark_map = {
        "line": {"type": "line", "point": True},
        "bar": {"type": "bar"},
        "histogram": {"type": "bar"},
        "pie": {"type": "arc"},
    }

    mark = mark_map.get(chart_type, {"type": "bar"})
    encoding = {}

    # Histogram
    if chart_type == "histogram":
        encoding["x"] = {
            "field": x_field,
            "type": "quantitative",
            "bin": True,
            "title": f"{x_field} ({infer_unit(x_field)})",
        }
        encoding["y"] = {
            "aggregate": "count",
            "type": "quantitative",
            "title": "Number of people",
        }

    # Pie
    elif chart_type == "pie":
        encoding["theta"] = {
            "aggregate": "count",
            "type": "quantitative",
            "title": "Number of people",
        }
        encoding["color"] = {
            "field": x_field,
            "type": "nominal",
            "legend": {"title": x_field},
        }

    # Line / Bar
    else:
        encoding["x"] = {
            "field": x_field,
            "type": infer_field_type(df[x_field]),
            "title": f"{x_field} ({infer_unit(x_field)})",
        }

        y_valid = field_is_valid(df, y_field)

        if aggregation == "count" or not y_valid:
            encoding["y"] = {
                "aggregate": "count",
                "type": "quantitative",
                "title": "Number of people",
            }
        else:
            encoding["y"] = {
                "field": y_field,
                "type": infer_field_type(df[y_field]),
                "aggregate": None
                if aggregation == "none"
                else aggregation,
                "title": f"{y_field} ({infer_unit(y_field)})",
            }

        color_field = viz.get("color")
        if chart_type == "bar" and field_is_valid(df, color_field):
            encoding["color"] = {
                "field": color_field,
                "type": "nominal",
                "legend": {"title": color_field},
            }

    confidence, reasons = compute_confidence(viz, df)

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
        "description": viz.get("description", ""),
        "mark": mark,
        "encoding": encoding,

        # UI metadata
        "confidence": confidence,
        "confidence_label": confidence_label(confidence),
        "confidence_reasons": reasons,
        "context": [
            viz.get("description", ""),
            "This chart highlights patterns derived from the uploaded dataset.",
        ],
    }