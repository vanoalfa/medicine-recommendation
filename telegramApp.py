import requests
from telegram.ext import Updater, MessageHandler, Filters

# Token bot kamu
BOT_TOKEN = "YOUR_BOT_TOKEN"
STREAMLIT_API_URL = "https://your-streamlit-app.streamlit.app/?q="

def handle(update, context):
    user_query = update.message.text
    try:
        response = requests.get(STREAMLIT_API_URL + user_query)
        # Ambil hasil sebagai teks
        html = response.text
        # Bisa parsing (pakai BeautifulSoup) atau cukup ambil bagian penting
        update.message.reply_text("✅ Hasil pencarian terkirim di Streamlit.\nLihat:\n" + STREAMLIT_API_URL + user_query)
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))
updater.start_polling()
