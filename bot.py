import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot operativo. ¡Hola Rubén!")

def check_sheet(update: Update, context: CallbackContext):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(config.SPREADSHEET_URL).sheet1
    data = sheet.get_all_records()
    update.message.reply_text(f"Productos encontrados: {len(data)}")

def main():
    updater = Updater(token=config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("check", check_sheet))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
