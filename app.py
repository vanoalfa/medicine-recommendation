from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
from VSMModel import VSMModel
import pandas as pd

TOKEN = "ISI_DENGAN_TOKEN_BOT_KAMU"  # Ganti token di sini
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Load dataset satu kali saat server di-start
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
        result_text = VSMModel(user_input, document_df=document_df)
        update.message.reply_text(result_text[:4090])  # Telegram max char = 4096
    except Exception as e:
        update.message.reply_text(f"Terjadi kesalahan:\n{str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
