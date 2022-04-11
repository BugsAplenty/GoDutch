# TODO: Get rid of the almost useless classes for the database and telegram functions.
import datetime

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from godutch_db import *
from utils import *

# Setup variables:
keyboard = [[
    InlineKeyboardButton("Get total for the month", callback_data='get_total_this_month')
]]
reply_markup = InlineKeyboardMarkup(keyboard)

config, db_config, whitelist = load_config()
connection = connect_db(db_config)


def get_all_totals_str(month, year):
    transaction_total_str = ""
    for user_id, username in get_all_user_ids(connection), get_all_usernames(connection):
        user_monthly_total = get_user_monthly_total(connection, user_id, month, year)
        transaction_total_str += f"{username} - {user_monthly_total}\n"
    return transaction_total_str


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi there! What would you like to add?')


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        'To add new transactions, just write them down in the following format: <transaction> - <amount>.',
        reply_markup=reply_markup
    )


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'get_total_this_month':
        now = datetime.datetime.now()  # TODO: Crappy. Can't get time from callback query so I have to rely on system time.
        query.message.reply_text(
            "Here's your total for the month: \n" + get_all_totals_str(now.month, now.year)
        )
    elif query.data == 'get_total_other_month':
        raise NotImplementedError


def handle_text(update: Update, context: CallbackContext):
    transaction_name, transaction_amount = parse_transaction_input(update)
    process_transaction(update, transaction_name, transaction_amount)


def main() -> None:
    updater = Updater(config["token"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start, Filters.user(user_id=whitelist)))
    dispatcher.add_handler(CallbackQueryHandler(button, Filters.user(user_id=whitelist)))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command & Filters.user(user_id=whitelist), handle_text))
    dispatcher.add_handler(CommandHandler('help', help_command))
    updater.start_polling()
    updater.idle()


def parse_transaction_input(update):
    try:
        transaction_name, transaction_amount = update.message.text.split('-')
        return transaction_name, transaction_amount
    except ValueError:
        update.message.reply_text(
            "Invalid text input. Please adhere to the format (<transaction> - <amount>).",
            reply_markup=reply_markup
        )
        return


def process_transaction(update, transaction_name, transaction_amount):
    try:
        transaction_amount = float(transaction_amount)
        add_transaction(
            connection,
            user_id=update.message.from_user.id,
            transaction_name=transaction_name,
            transaction_amount=transaction_amount,
            transaction_date=update.message.date
        )
        update.message.reply_text(
            "Transaction added. Add another or choose one of the menu items below:",
            reply_markup=reply_markup
        )
    except ValueError:
        update.message.reply_text(
            "Invalid text input. Please make sure you write a number left of the colon.",
            reply_markup=reply_markup
        )
        return


if __name__ == '__main__':
    main()
