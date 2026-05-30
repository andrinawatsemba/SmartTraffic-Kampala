# graph_utils.py
import osmnx as ox
import numpy as np
import json

def load_graph_nodes():
    G = ox.load_graphml("../data/raw/kampala_graph.graphml")
    nodes, _ = ox.graph_to_gdfs(G)
    
    node_ids = list(G.nodes())
    
    node_list = []
    for i, node_id in enumerate(node_ids):
        row = nodes.loc[node_id]
        node_list.append({
            "id": str(node_id),
            "lat": float(row.geometry.y),
            "lon": float(row.geometry.x)
        })
    
    return node_list, node_ids