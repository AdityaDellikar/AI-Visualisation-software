import pandas as pd

def profile_dataframe(df: pd.DataFrame) -> str:
    lines = []
    lines.append(f"Rows: {len(df)}")
    lines.append("Columns and types:")

    for col in df.columns:
        lines.append(f"- {col}: {df[col].dtype}")

    lines.append("\nBasic statistics:")
    try:
        stats = df.describe(include="all").transpose()
        lines.append(stats.head(10).to_string())
    except Exception:
        lines.append("Statistics not available.")

    lines.append("\nMissing values:")
    missing = df.isna().sum()
    lines.append(missing[missing > 0].to_string() or "No missing values")

    return "\n".join(lines)