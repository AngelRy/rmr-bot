import joblib
import torch
from sentence_transformers import SentenceTransformer

SIMILARITY_THRESHOLD = 0.532

# Lazy-loaded singletons
_model = None
_centroid = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    return _model


def _get_centroid():
    global _centroid
    if _centroid is None:
        centroid = joblib.load("running_centroid.joblib")

        if not isinstance(centroid, torch.Tensor):
            centroid = torch.tensor(centroid)

        _centroid = centroid / centroid.norm()

    return _centroid



def classify_quotes_batch(texts: list[str]):
    model = _get_model()
    centroid = _get_centroid()

    embeddings = model.encode(
        texts,
        convert_to_tensor=True,
        show_progress_bar=False  # disable tqdm spam
    )

    embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)

    scores = torch.matmul(embeddings, centroid)

    results = []

    for score in scores:
        value = score.item()
        results.append((value, value >= SIMILARITY_THRESHOLD))

    return results