from flask import Flask, request
import pandas as pd
import requests
from vsm_model import VSMModel

app = Flask(__name__)

TOKEN = "7998502915:AAHBzZc09gkTvGHOn0r8ZHbn2EC7B39yDPs"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Load data
document_df = pd.read_csv("product_preprocessed.csv")
document_df['product_preprocessed'] = document_df['product_preprocessed'].apply(eval)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        query = data["message"].get("text", "")

        # Jalankan VSMModel
        results = VSMModel(Pencarian, document_df)

        if results.empty:
            reply = "Maaf, tidak ditemukan produk yang relevan."
        else:
            top = results.iloc[0]
            reply = (
                f"🔍 *Hasil Pencarian Obat:*\n"
                f"*{top['title']}* (Similarity: {top['similarity']:.2f})\n"
                f"{top['original_text']}\n"
                f"[Link Produk]({top['url']})"
            )

        requests.post(URL, json={
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
        })

    return {"ok": True}
