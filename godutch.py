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
import json

def run(config, whitelist):
    pass


class GoDutch:
    def __init__(self):
        config_file = open('config.json')
        config = json.load(config_file)

        self.token = config['token']
        self.db = GoDutchDatabase(config)

        self.dispatcher = None
        self.updater = None

        self.keyboard = [[
            InlineKeyboardButton("Get total for the month", callback_data='get_total_this_month')
        ]]
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)

    def get_all_totals_str(self, month, year):
        transaction_total_str = ""
        for user_id, username in self.db.get_user_ids(), self.db.get_usernames():
            now = datetime.datetime.now()
            user_monthly_total = self.db.get_user_monthly_total(user_id, month, year)
            transaction_total_str += f"{username} - {user_monthly_total}\n"
        return transaction_total_str

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text('Hi there! What would you like to add?')

    def help_command(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'To add new transactions, just write them down in the following format: <transaction> - <amount>.',
            reply_markup=self.reply_markup
        )

    def button(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        if query.data == 'get_total_this_month':
            now = datetime.datetime.now()  # TODO: Crappy. Can't get time from callback query so I have to rely on system time.
            query.message.reply_text(
                "Here's your total for the month: \n" + self.get_all_totals_str(now.month, now.year)
            )
        elif query.data == 'get_total_other_month':
            raise NotImplementedError

    def handle_text(self, update: Update, context: CallbackContext):
        transaction_name, transaction_amount = self.parse_transaction_input(update)
        self.process_transaction(update, transaction_name, transaction_amount)

    def run(self, config, whitelist: list) -> None:
        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher

        self.updater.dispatcher.add_handler(CommandHandler('start', self.start, Filters.user(user_id=whitelist)))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button, Filters.user(user_id=whitelist)))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help_command))

        self.updater.start_polling()
        self.updater.idle()

    def parse_transaction_input(self, update):
        try:
            transaction_name, transaction_amount = update.message.text.split('-')
            return transaction_name, transaction_amount
        except ValueError:
            update.message.reply_text(
                "Invalid text input. Please adhere to the format (<transaction> - <amount>).",
                reply_markup=self.reply_markup
            )
            return

    def process_transaction(self, update, transaction_name, transaction_amount):
        try:
            transaction_amount = float(transaction_amount)
            self.db.add_transaction(
                user_id=update.message.from_user.id,
                transaction_name=transaction_name,
                transaction_amount=transaction_amount,
                transaction_date=update.message.date
            )
            update.message.reply_text(
                "Transaction added. Add another or choose one of the menu items below:",
                reply_markup=self.reply_markup
            )
        except ValueError:
            update.message.reply_text(
                "Invalid text input. Please make sure you write a number left of the colon.",
                reply_markup=self.reply_markup
            )
            return
