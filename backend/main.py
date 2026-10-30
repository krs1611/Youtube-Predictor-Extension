from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from feature_engineering import extract_title_features

app = FastAPI(
    title="YouTube Video Potential Predictor API",
    version="1.0.0",
    description="Machine Learning inference service for predicting YouTube video performance"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(base_dir, "model.joblib"))
feature_names = joblib.load(os.path.join(base_dir, "features.joblib"))

class VideoPredictRequest(BaseModel):
    title: str
    duration_minutes: float = 10.0
    tags_count: int = 10
    publish_hour: int = 18
    publish_dayofweek: int = 4

@app.get("/")
def health_check():
    return {"status": "online", "service": "YouTube Predictor API", "version": "1.0.0"}

@app.post("/predict")
def predict_video(payload: VideoPredictRequest):
    title_feats = extract_title_features(payload.title)
    is_weekend = 1 if payload.publish_dayofweek >= 5 else 0

    row_dict = {
        "duration_seconds": int(payload.duration_minutes * 60),
        "tags_count": payload.tags_count,
        "publish_hour": payload.publish_hour,
        "publish_dayofweek": payload.publish_dayofweek,
        "is_weekend": is_weekend,
        **title_feats
    }

    input_df = pd.DataFrame([row_dict])[feature_names]
    prob_high = float(model.predict_proba(input_df)[0][1])
    score_pct = round(prob_high * 100, 1)

    tier = "High Potential" if score_pct >= 60 else ("Moderate Potential" if score_pct >= 40 else "Standard Reach")

    suggestions = []
    if title_feats["title_caps_ratio"] < 0.15:
        suggestions.append("Capitalize key impact terms (e.g., '10 AI Tools You MUST Try').")
    if not title_feats["title_has_power_word"]:
        suggestions.append("Incorporate a high-curiosity hook keyword (e.g. 'Ultimate', 'Secret', 'Must').")
    if not title_feats["title_has_digits"]:
        suggestions.append("Adding specific numbers (e.g., '5 Mistakes', 'in 2026') increases click-through rates.")
    if payload.duration_minutes < 3.0:
        suggestions.append("Longer videos (8-15 mins) generally generate higher algorithmic watch time.")

    return {
        "success": True,
        "score_percentage": score_pct,
        "tier": tier,
        "title_features": title_feats,
        "suggestions": suggestions
    }
