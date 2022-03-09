from GoDutchDatabase import GoDutchDatabase
from enum import Enum
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
    Filters
)

class ButtonOptions(Enum):
    GET_TOTAL = 1
    GET_ANALYTICS = 2

class GoDutch:
    def __init__(self, token):
        self.dispatcher = None
        self.updater = None
        self.last_update = None
        self.token = token
        self.db = GoDutchDatabase()

        self.keyboard = [
            InlineKeyboardButton("Get total for the month", callback_data=ButtonOptions.GET_TOTAL)
        ]
        self.reply_markup = InlineKeyboardMarkup(self.keyboard)

    def expense_total_str(self):
        expense_total_str = ""
        for usr in self.db.users:
            expense_total_str += f"{usr} - {self.db.get_monthly_total(usr, self.last_update.message.date.month)}"
        return expense_total_str

    def start(self, update: Update):
        self.last_update = update
        update.message.reply_text('Hi there! What would you like to add?')

    def help_command(self, update: Update):
        self.last_update = update
        update.message.reply_text(
            'To add new expenses, just write them down in the following format: <expense> - <amount>.',
            reply_markup=self.reply_markup
        )

    def button(self, update: Update):
        self.last_update = update
        query = update.callback_query
        query.answer()
        if query.data == ButtonOptions.GET_TOTAL:
            query.message.reply_text("Here's your total for the month: \n" + self.expense_total_str())

    def handle_text(self, update: Update):
        self.last_update = update
        try:
            expense_name, expense_amount = update.message.text.split(' - ')
        except ValueError:
            update.message.reply_text(
                "Invalid text input. Please adhere to the format (<expense> - <amount>).",
                reply_markup=self.reply_markup
            )
            return
        try:
            expense_amount = float(expense_amount)
            self.db.append_expense(update.message.from_user.username, expense_name, expense_amount, self.last_update)
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


