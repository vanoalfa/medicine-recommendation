from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
from VSMModel import VSMModel
import pandas as pd
import os

TOKEN = os.environ.get("API_TELEGRAM")  # Gunakan variabel lingkungan di Render
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Load dataset satu kali saat server start
document_df = pd.read_csv("product_preprocessed.csv")

@app.route("/")
def index():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    dispatcher.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    dispatcher.process_update(update)
    return "ok", 200

def handle_message(update, context):
    user_input = update.message.text
    try:
        result_df = VSMModel(user_input, document_df=document_df)
        if result_df.empty:
            update.message.reply_text("Maaf, tidak ada dokumen yang relevan ditemukan.")
        else:
            response_text = ""
            for _, row in result_df.head(3).iterrows():  # Batasin 3 hasil
                response_text += f"📌 *{row['title']}*\n🔗 {row['url']}\n🔍 {row['original_text']}\n\n"
            update.message.reply_text(response_text[:4090])  # Telegram limit
    except Exception as e:
        update.message.reply_text(f"❌ Terjadi kesalahan:\n{str(e)}")

# Jalankan server Flask dengan port dari Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
