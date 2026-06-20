import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api import score_influencer_payload

app = FastAPI(title="VidGram Fraud Detection API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'data', 'merged', 'creator_dataset.json')
    if not os.path.exists(dataset_path):
        return []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/api/analyze/{username}")
def analyze_influencer(username: str):
    dataset = load_dataset()
    
    # Find the creator
    creator_data = next((c for c in dataset if c["username"].lower() == username.lower()), None)
    
    if not creator_data:
        raise HTTPException(status_code=404, detail="Creator not found")
        
    # Inject campaign mock since it might be requested by detectors
    creator_data["campaign"] = {
        "budget": 250000,
        "target_audience": "India",
        "category": "General"
    }
        
    # Run scoring engine
    result = score_influencer_payload(creator_data)
    
    # Format the required response
    return {
        "username": creator_data["username"],
        "followers": creator_data["followers"],
        "engagement_rate": creator_data.get("engagement_rate", 0),
        "authenticity_score": result.get("authenticity_score", 0),
        "risk_level": result.get("risk_level", "Unknown"),
        "fraud_probability": result.get("ml_risk", {}).get("fraud_probability", 0),
        "evidence": result.get("evidence", []),
        "alerts": result.get("alerts", [])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
