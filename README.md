# SmartTraffic Kampala

A hybrid GNN+LSTM traffic prediction system for Kampala, Uganda.
Built for the Ministry of ICT and National Guidance  Government Systems Prototype Showcase 2026.

## What it does
Predicts road congestion across Kampala's 17,762 road nodes using:
- **GNN (GraphSAGE)** — learns spatial dependencies between connected roads
- **LSTM** — learns temporal patterns (rush hours, weekly cycles)

## Results
- MAE: 0.0813 | RMSE: 0.1018 ( trained on simulated data)
- 17,762 nodes | 40,287 road segments
- 168 hourly timesteps (1 week)

## Stack
- Model: PyTorch + PyTorch Geometric
- Data: OpenStreetMap via OSMnx
- Backend: FastAPI
- Frontend: Leaflet.js

## Run locally

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
Open `frontend/index.html` in your browser.

## Area of interest
Interoperability & Data Exchange | Monitoring & Evaluation Systems

## Contact
Andrina Watsemba | Uganda Christian University | andrinawatsemba@gmail.com | +256 765982302
