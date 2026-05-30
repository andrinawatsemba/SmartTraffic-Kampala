# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from predict import load_model, predict
from graph_utils import load_graph_nodes

app = FastAPI(title="SmartTraffic Kampala API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load everything once at startup
print("Loading model and graph...")
model, edge_index_tensor = load_model()
node_list, node_ids = load_graph_nodes()
X = np.load("../data/processed/node_features.npy")
print(f"Ready. {len(node_list)} nodes loaded.")

@app.get("/")
def root():
    return {"status": "SmartTraffic Kampala API is running"}

@app.get("/predict/{timestep}")
def get_predictions(timestep: int):
    if timestep < 0 or timestep >= len(X):
        return {"error": f"Timestep must be between 0 and {len(X)-1}"}
    
    preds = predict(model, edge_index_tensor, X[timestep])
    
    result = []
    for i, node in enumerate(node_list):
        if i >= len(preds):
            break
        result.append({
            "id": node["id"],
            "lat": node["lat"],
            "lon": node["lon"],
            "congestion": round(preds[i], 4)
        })
    
    return {"timestep": timestep, "nodes": result}

@app.get("/timesteps")
def get_timesteps():
    return {"total_timesteps": len(X), "description": "168 hours (1 week)"}