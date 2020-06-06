from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import logging
from gerkules_mongodb import (GerkulesMongodb, GerkulesFood)

bot_token = '1260422753:AAGk_W_MfVoCD-HqTp54cAqTGay34Ll4gs8'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
gerkules_database = GerkulesMongodb()

SET_CALORIES, INPUT_MEAL = range(2)


def start(update, context):
    global gerkules_database
    user = update.message.from_user
    gerkules_database.add_user(user)

    logger.info(f"Started conversation with ***REMOVED***user.username***REMOVED***.")

    keyboard = [['Start my plan!'], ['Help']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Hi! What would you like to do?', reply_markup=markup)

    return SET_CALORIES


def set_calories(update, context):
    user = update.message.from_user
    logger.info(f"***REMOVED***user.username***REMOVED*** is inputting their calorie quota.")

    update.message.reply_text('Please tell me your goal. Insert how many calories do you want to consume per day.')
    if is_string_int(update.message.text):
        logger.info(update.message.text)
        return INPUT_MEAL


def stop(update, context):
    update.message.reply_text('Bye!')
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text('Help!')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def input_meal(update, context):
    user = update.message.from_user
    update.message.reply_text('What did you eat?')
    return ConversationHandler.END



def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states=***REMOVED***
            SET_CALORIES: [MessageHandler(Filters.text, set_calories)],
            INPUT_MEAL: [MessageHandler(Filters.text, input_meal)]
        ***REMOVED***,
        fallbacks=[CommandHandler('stop', stop)],
        name="my_conversation",

    )
    dp.add_handler(conv_handler)

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def is_string_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    main()
