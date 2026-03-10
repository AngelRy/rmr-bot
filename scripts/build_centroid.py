from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import joblib

# Load anchor quotes
df = pd.read_csv("data/distance_running_anchor_quotes.csv")
texts = df["text"].tolist()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(texts)

# Normalize embeddings
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# Compute centroid
centroid = np.mean(embeddings, axis=0)

# Normalize centroid
centroid = centroid / np.linalg.norm(centroid)

# Save artifacts
joblib.dump(centroid, "running_centroid.joblib")
joblib.dump(model, "embedding_model.joblib")

print("Centroid built successfully.")