from databases import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
bot_token = '1260422753:AAGk_W_MfVoCD-HqTp54cAqTGay34Ll4gs8'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')
    user = update.message.from_user
    users.append_row([user['username'], user['id']])

def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()