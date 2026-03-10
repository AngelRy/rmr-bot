from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
from rmrbot.database.models import get_all_quotes

# Load artifacts
centroid = joblib.load("running_centroid.joblib")
model = joblib.load("embedding_model.joblib")

quotes = get_all_quotes()

ids = [q[0] for q in quotes]
texts = [q[1] for q in quotes]

# Embed and normalize
embeddings = model.encode(texts)
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

# Cosine similarity
similarities = embeddings @ centroid

# Sort by similarity
pairs = list(zip(texts, similarities))
pairs_sorted = sorted(pairs, key=lambda x: x[1])
'''
print("\nLowest similarity examples:")
for t, s in pairs_sorted[:10]:
    print(round(s, 3), " | ", t[:80])

print("\nHighest similarity examples:")
for t, s in pairs_sorted[-10:]:
    print(round(s, 3), " | ", t[:80])


print("Min:", np.min(similarities))
print("Max:", np.max(similarities))
print("Mean:", np.mean(similarities))
print("Std:", np.std(similarities))

percentiles = np.percentile(similarities, [5, 10, 25, 50, 75, 90, 95])
print("Percentiles (5,10,25,50,75,90,95):")
print(percentiles)


for t, s in pairs_sorted:
    if 0.43 <= s <= 0.53:
        print(round(s,3), "|", t[:120])

import numpy as np
'''
SIMILARITY_THRESHOLD = 0.532  # your proposed value

similarities = np.array(similarities)

kept = np.sum(similarities >= SIMILARITY_THRESHOLD)

print(f"Threshold: {SIMILARITY_THRESHOLD}")
print(f"Kept: {kept} / {len(similarities)}")
print(f"Retention: {kept / len(similarities):.2%}")