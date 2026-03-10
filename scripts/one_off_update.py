from sentence_transformers import SentenceTransformer
import joblib
import torch


from rmrbot.database.models import get_all_quotes, update_similarity

SIMILARITY_THRESHOLD = 0.532

print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Loading centroid...")
centroid = joblib.load("running_centroid.joblib")

# convert to torch tensor if it was saved as numpy
if not isinstance(centroid, torch.Tensor):
    centroid = torch.tensor(centroid)

centroid = centroid / centroid.norm()

quotes = get_all_quotes()
texts = [q["text"] for q in quotes]

print("Embedding quotes...")
embeddings = model.encode(texts, convert_to_tensor=True)

print("Updating database...")

for quote, emb in zip(quotes, embeddings):
    emb = emb / emb.norm()
    score = torch.dot(emb, centroid).item()
    is_relevant = score >= SIMILARITY_THRESHOLD

    update_similarity(
        quote_id=quote["id"],
        score=score,
        is_relevant=is_relevant
    )

print("Done.")