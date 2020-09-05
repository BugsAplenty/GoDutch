#!/usr/bin/env python

import logging
from telegram import InlineQueryResult
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters,
                          ConversationHandler, InlineQueryHandler)
from databases.user_database import gerkules_user_db
from databases.food_database import gerkules_food_db
from utils.keyboards import *


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

[START, SET_TIMEZONE, SET_GOAL, START_PLAN, INPUT_MEAL, INPUT_CANCELLED, QUOTA_EXCEEDED, SUMMARIZE_INPUT,
 INPUT_ACCEPTED, INPUT_ACCEPTED_QUOTA_EXCEEDED, NEW_FOOD_CAL_CHECK, AMOUNT_CHECK] = range(12)


def start(update, context):
    text = f'Welcome, ***REMOVED***update.message.from_user.username***REMOVED***!\n'\
           f'My name is Gerkules. I can count your daily calorie intake!\n'\
           f'What would you like to do?'
    update.message.reply_text(text=text, reply_markup=START_SELECT)
    return SET_TIMEZONE


def help(args):
    pass


def timezone_select(update, context):
    text = f"Before we begin, please tell me what timezone you're in. I will reset your calorie limit at midnight."
    update.message.reply_text(text=text, reply_markup=START_SELECT)
    return SET_GOAL


def main():
    updater = Updater("1390293873:AAHuLppubBQqfBVWgswQD8u6dKupXhzxtF4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states=***REMOVED***
            SET_TIMEZONE: [CallbackQueryHandler(timezone_select, pattern='(?!' + str(SET_PLAN_BUTTON.callback_data) + ').*$')],
            SET_GOAL: [InlineQueryHandler(timezone_select, pattern='[+-][0-9]***REMOVED***2***REMOVED***:[0-9]***REMOVED***2***REMOVED***\b')]
        ***REMOVED***,

        fallbacks=[CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
