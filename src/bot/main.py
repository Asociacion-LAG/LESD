
from os import system

from dotenv import load_dotenv
from dotenv.main import dotenv_values
from mariadb import Error, connect, connection
from telebot import TeleBot

import messages

load_dotenv()

# Connection to telegram
lesd = TeleBot(dotenv_values().get("TOKEN"))

# Message handler
lesdMessages = messages.Messages(lesd)

# DB connection
try:
    connection = connect(
        user=dotenv_values().get("DB_USER"),
        password=dotenv_values().get("DB_PSSW"),
        host=dotenv_values().get("HOST"),
        database=dotenv_values().get("DB")
    )
    print("Connected to database")
except Error as e:
    print(f"Database error: {e}")
    exit()

# COMMAND HANDLERS


@lesd.message_handler(commands=['start'])  # Start
def start(message):
    lesdMessages.sendStartMessage(message)


@lesd.message_handler(commands=['help'])  # Help
def help(message):
    lesdMessages.sendHelpMessage(message)


@lesd.message_handler(commands=['new'])  # New
def new(message):
    lesdMessages.addNewBooth(message, connection)


# Message Not Recogniced
@lesd.message_handler(func=lambda message: True, content_types=['text'])
def undefinedMessage(message):
    lesdMessages.messageNotRecogniced(message)


@lesd.message_handler(commands=['book'])  # Book
def book(message):
    lesdMessages.bookMessage(message)


@lesd.callback_query_handler(func=lambda call=True)
def query_handler(call):
    if("next_" in call.data):
        # next command
    elif("book_" in call.data):
        # book command


try:
    lesd.polling()
except Exception as e:
    print(f'Bot error: {e}')
    exit()
