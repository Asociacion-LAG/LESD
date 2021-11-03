
from os import system

from dotenv import load_dotenv
from dotenv.main import dotenv_values
from mariadb import Error, connect, connection
from telebot import TeleBot, types

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


# Start
@lesd.message_handler(commands=['start'])
def start(message):
    lesdMessages.sendStartMessage(message)


# Help
@lesd.message_handler(commands=['help'])
def help(message):
    lesdMessages.sendHelpMessage(message)


# New
@lesd.message_handler(commands=['new'])
def new(message):
    lesdMessages.addNewBooth(message, connection)


# Book
@lesd.message_handler(commands=['book'])
def book(message):
    lesdMessages.bookMessage(message, connection)


# Cancel
@lesd.message_handler(commands=['cancel'])
def cancel(message):
    lesdMessages.cancelMessage(message, connection)


# Next
@lesd.message_handler(commands=['next'])
def next(message):
    lesdMessages.nextMessage(message, connection)


# Data
@lesd.message_handler(commands=['data'])
def dataStored(message):
    lesdMessages.dataMessage(message)

# Enable event


@lesd.message_handler(commands=['enable'])
def enableEvent(message):
    lesdMessages.enableMessage(message, connection)

# Disable event


@lesd.message_handler(commands=['disable'])
def enableEvent(message):
    lesdMessages.disableMessage(message, connection)

# Message Not Recogniced


@lesd.message_handler(func=lambda message: True, content_types=['text'])
def undefinedMessage(message):
    lesdMessages.messageNotRecogniced(message)


@lesd.callback_query_handler(func=lambda call: True)  # Button Handler
def query_handler(call: types.CallbackQuery):
    if("book_" in call.data):
        booth = call.data.replace('book_', '')
        lesdMessages.booking(
            booth=booth, message=call.message, connection=connection)
    elif('cancel_' in call.data):
        booth = call.data.replace('cancel_', '')
        lesdMessages.cancel(
            booth=booth, message=call.message, connection=connection)
    elif('next_' in call.data):
        booth = call.data.replace('next_', '')
        lesdMessages.next(booth=booth, message=call.message,
                          connection=connection)
    elif('enable_' in call.data):
        booth = call.data.replace('enable_', '')
        lesdMessages.enableEvent(
            booth=booth, message=call.message, connection=connection)
    elif('disable_' in call.data):
        booth = call.data.replace('disable_', '')
        lesdMessages.disableEvent(
            booth=booth, message=call.message, connection=connection)


try:
    lesd.polling()
except Exception as e:
    print(f'Bot error: {e}')
    exit()
