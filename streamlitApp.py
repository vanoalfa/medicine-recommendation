import streamlit as st
import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Load model dan data
@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

@st.cache_data
def load_data():
    df = pd.read_csv("product_preprocessed.csv")
    return df

embedding_model = load_model()
df = load_data()

# Encode semua dokumen sekali saja
@st.cache_data
def encode_documents(documents):
    return embedding_model.encode(documents)

doc_texts = df['product_preprocessed'].tolist()
document_embeddings = encode_documents(doc_texts)

# UI atau query param
query = st.query_params.get('q') or st.text_input("Masukkan pertanyaan obat:")

def search(query):
    tokenized_query = word_tokenize(query)
    query_text = ' '.join(tokenized_query)
    query_vec = embedding_model.encode([query_text])[0]
    scores = cosine_similarity([query_vec], document_embeddings)[0]

    results = []
    for i, score in enumerate(scores):
        if score > 0.55:
            results.append({
                'title': df.iloc[i]['title'],
                'similarity': score,
                'url': df.iloc[i]['url'],
                'text': df.iloc[i]['full_artikel'][:150] + '...',
            })
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:3]

if query:
    results = search(query)
    for res in results:
        st.write(f"**{res['title']}**")
        st.write(f"🔗 {res['url']}")
        st.write(res['text'])
        st.write("---")
