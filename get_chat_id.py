from dotenv import load_dotenv
from os import getenv
from telebot import TeleBot

load_dotenv()


TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")

# Create a bot instance
bot = TeleBot(TELEGRAM_TOKEN)


# Define a handler for the "/start" command
@bot.message_handler(commands=["id"])
def start(message):
    # Get the chat ID of the current message
    chat_id = message.chat.id
    # Check if the chat is a group or supergroup
    if message.chat.type in ["group", "supergroup"]:
        # Process the group chat ID
        print("Group ID:", chat_id)
        bot.send_message(chat_id, f"Group ID: `{chat_id}`", parse_mode="MARKDOWN")


# Start the bot
bot.polling()
