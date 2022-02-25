#imports
import logging
import os
import mathbot
import parser
import wolfram

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# inline query imports
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

import dotenv
from dotenv import load_dotenv

#Strings
START = "Hi! I'm b24ac, a math bot. Please send me your math problems, I will try to solve them for you using Python's eval function or Wolfram Alpha."
HELP = "I use Python's eval by default, to use Wolfram, start the query with /wolf."
ERROR = "Invalid input, Please input a mathematical formula"

# Add your bot's token from botfather in the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=START)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(HELP)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

########################################################################    
                        ###  ADDED FUNCTIONS ###
########################################################################    

# Run with /math command
def basicCalcText_cmd(update: Update, context: CallbackContext) -> None:
    try:
        input = ' '.join(context.args)
        parsed = parser.parse(input)
        response = input + " = " + mathbot.calc(parsed)
        update.message.reply_text(response)
    except:
        update.message.reply_text(ERROR)
        
def basicCalcText(update: Update, context: CallbackContext) -> None:
    try:
        input = update.message.text
        parsed = parser.parse(input)
        response = "Python Eval: \n" + input + " = " + mathbot.calc(parsed)
        update.message.reply_text(response)
    except:
        update.message.reply_text(ERROR)
        
def wolframQuery(update: Update, context: CallbackContext) -> None:
    try:
        input = update.message.text
        
        parsed = parser.parse(input)
        
        response = "Wolfram Alpha: \n" + wolfram.waquery(parsed)
        update.message.reply_text(response)
    except:
        update.message.reply_text("wolfram query failed")
        
def wolframQuery_cmd(update: Update, context: CallbackContext) -> None:
    try:
        input = ' '.join(context.args)
        parsed = parser.parse(input)
        response = "Wolfram Alpha: \n" + wolfram.waquery(parsed)
        update.message.reply_text(response)
    except:
        update.message.reply_text("wolfram query failed")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("math", basicCalcText_cmd))
    dispatcher.add_handler(CommandHandler("wolf", wolframQuery_cmd))

    # on non command i.e message - evaluate input string
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, basicCalcText))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()