import umap
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_articles(texts):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    clean_texts = [t.strip() for t in texts if t and len(t.strip()) > 5]
    if not clean_texts:
        return None
    embeddings = model.encode(clean_texts)
    return embeddings




def reduce_dimensions(embeddings, n_neighbors=5, min_dist=0.3):
    if embeddings.shape[0] < 5:
        # Not enough data for UMAP — fallback to PCA
        reducer = PCA(n_components=2)
        embedding_2d = reducer.fit_transform(embeddings)
        return embedding_2d
    else:
        reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, metric="cosine")
        embedding_2d = reducer.fit_transform(embeddings)
        return embedding_2d
