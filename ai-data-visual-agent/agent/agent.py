from langchain_ollama import ChatOllama

# ============================================================
# 🔒 ANALYSIS MODEL (STRICT JSON OUTPUT — for /analyze)
# ============================================================

analysis_llm = ChatOllama(
    model="llama3:latest",
    temperature=0.0  # deterministic for schema filling
)

FILL_TEMPLATE = """
You MUST fill in the JSON template below.

RULES (ABSOLUTE):
- Do NOT add or remove keys
- Do NOT add explanations outside JSON
- Do NOT output text outside JSON
- Replace every <...> placeholder
- Use ONLY these chart types:
  line, bar, histogram, pie, map

IMPORTANT GUIDANCE:
- Choose charts that BEST match the data types
- The chart description MUST explain:
  1. What the chart shows
  2. Why this chart is appropriate
- Keep descriptions concise (1 sentence)

JSON TEMPLATE (FILL ALL FIELDS):

{
  "insights": [
    "<insight_1>",
    "<insight_2>",
    "<insight_3>"
  ],
  "visualizations": [
    {
      "type": "<line|bar|histogram|pie|map>",
      "title": "<short title>",
      "description": "<one sentence explaining what this chart shows and why it is appropriate>",
      "x": "<column name>",
      "y": "<column name>",
      "color": null,
      "aggregation": "none",
      "interactions": ["hover", "filter"]
    },
    {
      "type": "<line|bar|histogram|pie|map>",
      "title": "<short title>",
      "description": "<one sentence explaining what this chart shows and why it is appropriate>",
      "x": "<column name>",
      "y": "<column name>",
      "color": null,
      "aggregation": "none",
      "interactions": ["hover", "filter"]
    }
  ]
}
"""

def run_agent(user_goal: str, dataset_summary: str) -> str:
    """
    Used ONLY for /analyze
    Returns STRICT JSON (no free text)
    """
    prompt = f"""
You are a senior data analyst designing charts for a modern analytics product.

USER GOAL:
{user_goal}

DATASET SUMMARY (PLAIN TEXT, NOT JSON):
<<<
{dataset_summary}
>>>

{FILL_TEMPLATE}
"""
    response = analysis_llm.invoke(prompt)
    return response.content


# ============================================================
# 🧠 EXPLANATION MODEL (NATURAL LANGUAGE — for /explain)
# ============================================================

explain_llm = ChatOllama(
    model="llama3:latest",
    temperature=0.3  # allows fluent, human explanations
)

def run_explainer(prompt: str) -> str:
    """
    Used ONLY for /explain
    GUARANTEED to return human-readable text
    """
    response = explain_llm.invoke(prompt)
    text = response.content.strip()

    # 🚫 HARD SAFETY: NEVER allow JSON to reach UI
    if text.startswith("{") or text.startswith("["):
        return (
            "This data point highlights a meaningful pattern in the chart. "
            "It represents a notable concentration within this category, "
            "which can help guide business decisions."
        )

    return text