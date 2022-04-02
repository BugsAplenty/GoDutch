import datetime

from GoDutchDatabase import GoDutchDatabase
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


class GoDutch:
    def __init__(self):
        config_file = open('config.json')
        config = json.load(config_file)

        self.token = config['token']
        self.db = GoDutchDatabase(config)

        self.dispatcher = None
        self.updater = None
        self.last_update = None

        self.keyboard = [[
            InlineKeyboardButton("Get total for the month", callback_data='get_total')
        ]]
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)

    def transaction_total_str(self):
        transaction_total_str = ""
        for usr in self.db.get_users():
            now = datetime.datetime.now()  # TODO: Crappy. Can't get time from callback query so I have to rely on system time.
            current_year = now.year
            current_month = now.month
            transaction_total_str += f"{usr} - {self.db.get_user_monthly_total(usr, current_month, current_year)}"
        return transaction_total_str

    def start(self, update: Update, context: CallbackContext):
        self.last_update = update
        update.message.reply_text('Hi there! What would you like to add?')

    def help_command(self, update: Update, context: CallbackContext):
        self.last_update = update
        update.message.reply_text(
            'To add new transactions, just write them down in the following format: <transaction> - <amount>.',
            reply_markup=self.reply_markup
        )

    def button(self, update: Update, context: CallbackContext):
        self.last_update = update
        query = update.callback_query
        query.answer()
        if query.data == 'get_total':
            query.message.reply_text("Here's your total for the month: \n" + self.transaction_total_str())

    def handle_text(self, update: Update, context: CallbackContext):
        self.last_update = update
        try:
            transaction_name, transaction_amount = update.message.text.split('-')
        except ValueError:
            update.message.reply_text(
                "Invalid text input. Please adhere to the format (<transaction> - <amount>).",
                reply_markup=self.reply_markup
            )
            return
        try:
            transaction_amount = float(transaction_amount)
            self.db.add_transaction(
                user_id=update.message.from_user.id,
                transaction_name=transaction_name,
                transaction_amount=transaction_amount,
                transaction_date=self.last_update.message.date
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

    def run(self) -> None:
        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher

        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help_command))

        self.updater.start_polling()
        self.updater.idle()
