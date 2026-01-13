from agent.agent import run_agent
from agent.json_utils import extract_json
from agent.normalizer import normalize_agent_output
from data.loader import load_excel
from data.profiler import profile_dataframe

df = load_excel("sample.xlsx")
summary = profile_dataframe(df)

raw_text = run_agent(
    user_goal="Find key insights and recommend the best visualizations",
    dataset_summary=summary
)

print("\n=== RAW AGENT TEXT ===\n")
print(raw_text)

try:
    raw_json = extract_json(raw_text)
except ValueError as e:
    print("\n⚠️ JSON extraction failed. Retrying with stricter prompt...\n")

    raw_text = run_agent(
        user_goal="Return ONLY valid JSON. Do not explain. Do not summarize.",
        dataset_summary=summary
    )

    print("\n=== RAW AGENT TEXT (RETRY) ===\n")
    print(raw_text)

    raw_json = extract_json(raw_text)

normalized = normalize_agent_output(raw_json)
print("\n=== RAW JSON ===\n")
print(raw_json)

print("\n=== NORMALIZED OUTPUT ===\n")
print(normalized)

from agent.vegalite import generate_vegalite_spec

print("\n=== VEGA-LITE SPECS ===\n")

for viz in normalized["visualizations"]:
    spec = generate_vegalite_spec(viz)
    print(spec)