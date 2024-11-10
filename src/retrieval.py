import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.neighbors import NearestNeighbors

BI_ENCODER_MODEL_ID = "intfloat/multilingual-e5-large"
CROSS_ENCODER_MODEL_ID = "BAAI/bge-reranker-large"

# Load chunks
df = pd.read_csv("corpus/chunks.csv")
chunks = []
chunks_text = []

for index, row in df.iterrows():
    chunk_text = f"Extracto de página web de título: {row['title']} - URL: {row['source']}\n{row['chunk']}"
    chunks.append({
        "title": row['title'],
        "source": row['source'],
        "chunk": chunk_text
    })
    chunks_text.append(chunk_text)

def initialize_model_bi_encoder(k=3):
    """Initialize the Bi-Encoder model.

    Parameters:
    - k: Int, the number of chunks to retrieve

    Returns:
    - model: Dict, the Bi-Encoder model and K-NN classifier
    """
    model_emb = SentenceTransformer(BI_ENCODER_MODEL_ID)

    # Generate embeddings for the chunks
    embeddings_chunks = model_emb.encode(chunks_text, normalize_embeddings=True)

    # K-NN classifier
    model_knn = NearestNeighbors(n_neighbors=k)
    model_knn.fit(embeddings_chunks)

    return {
        "model_emb": model_emb,
        "model_knn": model_knn
    }

def initialize_model_cross_encoder():
    """Initialize the Cross-Encoder model.

    Returns:
    - model: CrossEncoder, the Cross-Encoder model
    """
    return CrossEncoder(CROSS_ENCODER_MODEL_ID)


def retrieve(question, model):
    """Retrieve the references for a given question using the specified model.

    Parameters:
    - question: String, the question to retrieve the references for
    - model: Dict or CrossEncoder, the model to use for retrieval

    Returns:
    - references: List of Dict, the most similar chunks to the question
    """
    if isinstance(model, dict):
        return knn_retrieval(question, model)
    else:
        return ce_retrieval(question, model)

def knn_retrieval(question, model, k=3):
    """
    Retrieve the most similar chunks to a message.

    Parameters:
    - model: Dict, the Bi-Encoder model and K-NN classifier
    - question: String, the question to retrieve the most similar chunks for
    - k: Int, the number of chunks to retrieve

    Returns:
    - references: List of Dict}
    , the most similar chunks to the question
    """
    model_emb = model["model_emb"]
    model_knn = model["model_knn"]

    references_ids = model_knn.kneighbors(
        [model_emb.encode("query: " + question, normalize_embeddings=True)]
    )[1][0]

    references = [chunks[int(i)] for i in references_ids]

    return references

def ce_retrieval(question, model, k=3):
    """
    Retrieve the most similar chunks to a message using the Cross-Encoder model.

    Parameters:
    - model: CrossEncoder, the Cross-Encoder model
    - question: String, the question to retrieve the most similar chunks for
    - k: Int, the number of chunks to retrieve

    Returns:
    - references: List of Dict, the most similar chunks to the question
    """
    pairs = [(question, document) for document in chunks_text]
    scores = model.predict(pairs)
    ind = np.argpartition(scores, -k)[-k:]
    ind = ind[np.argsort(scores[ind])][::-1]
    return [chunks[i] for i in ind]