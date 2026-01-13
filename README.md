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
