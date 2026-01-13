from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import io
import math

from data.profiler import profile_dataframe
from agent.agent import run_agent, run_explainer
from agent.json_utils import extract_json
from agent.normalizer import normalize_agent_output
from agent.vegalite import generate_vegalite_spec


# ----------------------------
# Utils
# ----------------------------
def clean_for_json(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    return obj


app = FastAPI()


# ----------------------------
# ✅ CORS (FIXED FOR VERCEL)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# ANALYZE ENDPOINT
# ----------------------------
@app.post("/analyze")
async def analyze_excel(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    # Safe numeric coercion
    for col in df.columns:
        try:
            converted = pd.to_numeric(df[col])
            if converted.notna().sum() > 0:
                df[col] = converted
        except Exception:
            pass

    data_rows = clean_for_json(df.to_dict(orient="records"))
    summary = profile_dataframe(df)

    raw_text = run_agent(
        user_goal="Analyze the dataset and propose the best visualizations",
        dataset_summary=summary,
    )

    raw_json = extract_json(raw_text)
    normalized = normalize_agent_output(raw_json)

    specs = []
    for viz in normalized["visualizations"]:
        spec = generate_vegalite_spec(viz, df)
        if spec is not None:
            specs.append(spec)

    return clean_for_json(
        {
            "insights": normalized["insights"],
            "charts": specs,
            "data": data_rows,
        }
    )


# ----------------------------
# EXPLAIN ENDPOINT
# ----------------------------
class ExplainRequest(BaseModel):
    chart_description: str
    selected_value: dict


@app.post("/explain")
async def explain_point(payload: ExplainRequest):
    prompt = f"""
You are explaining a data point to a non-technical business user.

Chart context:
{payload.chart_description}

Selected data point:
{payload.selected_value}

RULES (ABSOLUTE):
- DO NOT return JSON
- DO NOT use bullet points
- DO NOT mention schemas, templates, or fields
- DO NOT restate the chart title
- Write 2–3 short sentences ONLY
- Explain what this data point means in plain business language
"""

    raw_text = run_explainer(prompt)

    return {"explanation": raw_text.strip()}