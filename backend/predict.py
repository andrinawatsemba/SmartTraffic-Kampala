# predict.py
import torch
import numpy as np
from torch_geometric.nn import SAGEConv
import torch.nn as nn

class GNN_LSTM(nn.Module):
    def __init__(self, num_nodes, input_dim, hidden_dim, lstm_hidden, output_dim):
        super(GNN_LSTM, self).__init__()
        self.gnn1 = SAGEConv(input_dim, hidden_dim)
        self.gnn2 = SAGEConv(hidden_dim, hidden_dim)
        self.lstm = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=lstm_hidden,
            num_layers=2,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(lstm_hidden, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x, edge_index):
        x = self.relu(self.gnn1(x, edge_index))
        x = self.relu(self.gnn2(x, edge_index))
        x = x.unsqueeze(0)
        lstm_out, _ = self.lstm(x)
        x = lstm_out.squeeze(0)
        return self.fc(x)

def load_model():
    edge_index = np.load("../data/processed/edge_index.npy")
    edge_index_tensor = torch.tensor(edge_index, dtype=torch.long)

    model = GNN_LSTM(
        num_nodes=17762,
        input_dim=1,
        hidden_dim=64,
        lstm_hidden=64,
        output_dim=1
    )
    model.load_state_dict(torch.load("../model/saved/smart_traffic_model.pt", map_location="cpu"))
    model.eval()

    return model, edge_index_tensor

def predict(model, edge_index_tensor, timestep_data):
    x = torch.tensor(timestep_data, dtype=torch.float32).unsqueeze(1)
    with torch.no_grad():
        out = model(x, edge_index_tensor)
    return out.numpy().flatten().tolist()