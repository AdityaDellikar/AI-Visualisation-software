# AI Data Visualization Platform

An AI-powered full-stack application that analyzes datasets and automatically generates meaningful, interactive visualizations with natural-language explanations.

---

## 🧠 What this project does
- Upload Excel datasets
- AI analyzes schema & patterns
- Automatically recommends charts
- Renders interactive Vega-Lite visualizations
- Explains selected data points in plain English
- Adds confidence scoring to each chart
<img width="1279" height="758" alt="Screenshot 2026-01-14 at 8 51 37 AM" src="https://github.com/user-attachments/assets/3a38e860-20be-4a15-8f33-130f22180f67" /><img width="1279" height="427" alt="Screenshot 2026-01-14 at 8 53 00 AM" src="https://github.com/user-attachments/assets/fff7101c-4ee1-43b0-b137-06eb8cfad6e7" />
<img width="1279" height="640" alt="Screenshot 2026-01-14 at 8 53 20 AM" src="https://github.com/user-attachments/assets/6bf5ec9f-b093-4842-a800-199879b6b44f" />
<img width="1279" height="683" alt="Screenshot 2026-01-14 at 8 53 32 AM" src="https://github.com/user-attachments/assets/474d24f4-4f8f-470d-b8c9-13b5e2f65794" />
<img width="1279" height="683" alt="Screenshot 2026-01-14 at 8 53 45 AM" src="https://github.com/user-attachments/assets/80343437-3231-45b9-932b-93db243a9633" />
<img width="1279" height="683" alt="Screenshot 2026-01-14 at 9 01 20 AM" src="https://github.com/user-attachments/assets/a107158f-ef70-4b95-b7d1-f69699737aab" />


---

## 🏗 Project Structure

aiViz/ 1. ai-data-visual-agent/   # Backend (FastAPI + AI) 2.viz-ui/                 # Frontend (React + Vega-Lite)

---

## 🧪 Tech Stack

### Backend
- Python
- FastAPI
- Pandas
- Vega-Lite spec generator
- LLaMA via Ollama

### Frontend
- React
- Vega-Lite / Vega-Embed
- Fetch API

---

## 🚀 Local Setup

### Backend
```bash
cd ai-data-visual-agent
uvicorn api:app --reload

cd viz-ui
npm install
npm start

⚠️ Requires Ollama running locally for AI features.

✨ Key Features
	•	AI-generated visualization recommendations
	•	Auto chart validation & confidence scoring
	•	Click-to-explain data points
	•	Robust handling of missing / noisy data
	•	Production-oriented architecture


📌 Status : Actively developed. Deployment coming soon.
