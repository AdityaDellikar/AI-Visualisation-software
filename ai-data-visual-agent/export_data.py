from data.loader import load_excel

df = load_excel("sample.xlsx")
df.to_json("../viz-ui/public/sample.json", orient="records")

print("✅ Data exported to viz-ui/public/sample.json")