import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json
import requests
import time
import random
# Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

ramzinexURL = "https://publicapi.ramzinex.com/exchange/api/v1.0/exchange/pairs?base_id=2"


def start(update: Update, context: CallbackContext) -> None:
    users: list = []
    with open('Bot/users.json', encoding="utf8") as f:
        users = json.load(f).get("users")
    savedData: dict = {}
    for key, value in update.message.chat.to_dict().items():
        savedData[key.strip()] = str(value).strip()
    users.append(savedData)
    res: list = []
    [res.append(x) for x in users if x not in res]
    res = {"users": res}
    with open('Bot/users.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=4))
    update.message.reply_text("""
    سلام
    عرفان نوربخش هستم:)
    قیمت لحظه ای ارز دیجیتال رو برات میگم
    راهنمای استفاده از بات :
    شروع دوباره بات => /start
    قیمت ارزهای دیجیتال => /price
    پشتیبانی => /help
    10/15/2021""")


def price(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    with open('ramzinex.json') as f:
        data = json.load(f)
    keyboard: list = []
    for i in range(len(data.get("data"))):
        keyboard.append([InlineKeyboardButton(
            str(data.get("data")[i].get("name").get("fa")), callback_data=str(i))])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'قیمت کدوم رو میخوای بدونی ؟ ', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    with open('ramzinex.json') as f:
        data = json.load(f)
    query.answer()
    w = """
            %s
            خرید : %s
            فروش : %s
            تغییر : %s
            """ % (data.get("data")[int(query.data)].get("name").get("fa"), data.get("data")[int(query.data)].get("sell"), data.get("data")[int(query.data)].get("buy"), data.get("data")[int(query.data)].get("financial").get("last24h").get("change_percent"))
    query.edit_message_text(text=w)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("برای استفاده از بات /start را وارد کنید :)")


def main() -> None:
    """Run the bot."""
    updater = Updater("2094043841:AAGVnQoXFMU8LJ63_zdzq2X2uvnxeJYc54o")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('price', price))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()
    # Ramzinex Data
    while True:
        response = requests.get(ramzinexURL)
        with open('ramzinex.json', 'w') as f:
            f.write(json.dumps(response.json()))
            randomData = random.randint(1, 5)
            print("data received")
            time.sleep(randomData)


if __name__ == '__main__':
    main()
