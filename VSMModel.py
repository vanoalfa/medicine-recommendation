import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

nltk.download('punkt')

def VSMModel(Pencarian, document_df=pd.read_csv('/content/product_preprocessed.csv')):
    #Instalasi model embedding
    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    #Ambil dokumen dari dataframe
    documents = document_df['product_preprocessed']

    #Proses Query
    query = Pencarian
    try:
        tokenized_query = word_tokenize(query)
    except:
        #Kalau NLTK gagal, pakau teknik splitting
        tokenized_query = query.split()

    #Gabung list jadi strings
    preprocessed_documents = [' '.join(doc) if isinstance(doc, list) else doc for doc in documents]
    preprocessed_query = ' '.join(tokenized_query) if isinstance(tokenized_query, list) else query

    #Encode document dan query
    document_embeddings = embedding_model.encode(preprocessed_documents)
    query_embedding = embedding_model.encode([preprocessed_query])[0]

    #Hitung cosine similarities
    cosine_similarities = cosine_similarity([query_embedding], document_embeddings)[0]

    #Buat hasilnya
    results = []
    for i, similarity in enumerate(cosine_similarities):
        if similarity > 0.55:  #Threshold 55%
            original_text = document_df.iloc[i].get('full_artikel', ' '.join(documents[i]) if isinstance(documents[i], list) else documents[i])

            doc_terms = set(documents[i]) if isinstance(documents[i], list) else set(word_tokenize(documents[i]))
            query_terms = set(tokenized_query)
            matching_terms = list(doc_terms.intersection(query_terms))

            results.append({
                'document_id': i,
                'title': document_df.iloc[i]['title'],
                'similarity': similarity,
                'matching_terms': matching_terms,
                'original_text': original_text[:150] + "..." if len(original_text) > 150 else original_text,
                'url' : document_df.iloc[i]['url']
            })



    #Buat dataframe berdasarkan simlirarity nya
    results_df = pd.DataFrame(results) if results else pd.DataFrame(
        columns=['document_id', 'similarity', 'matching_terms', 'original_text','url']
    )

    if not results_df.empty:
        results_df = results_df.sort_values(by='similarity', ascending=False).reset_index(drop=True)

    # Buat output teks
    output = f"\nVector Space Model Search Results for: '{Pencarian}'\n"
    output += f"Found {len(results_df)} relevant documents\n\n"

    if not results_df.empty:
        for idx, row in results_df.iterrows():
            output += f"Document {row['document_id']} - Similarity: {row['similarity']:.4f}\n"
            output += f"Medicine Title: {row['title']}\n"
            if row['matching_terms']:
                output += f"Lexical overlap terms: {', '.join(row['matching_terms'])}\n"
            output += f"Text: {row['original_text']}\n"
            output += f"Link: {row['url']}\n"
            output += "-" * 50 + "\n"
    else:
        output += "No relevant documents found.\n"

    return output
