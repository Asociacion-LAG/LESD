
from os import system

import mariadb
import telebot
from dotenv import load_dotenv
from dotenv.main import dotenv_values

import databaseManager
import messages

load_dotenv()

# Connection to telegram
lesd = telebot.TeleBot(dotenv_values().get("TOKEN"))

# Message handler
lesdMessages = messages.Messages(lesd)

# DB connection
try:
    connection = mariadb.connect(
        user=dotenv_values().get("DB_USER"),
        password=dotenv_values().get("DB_PSSW"),
        host=dotenv_values().get("HOST"),
        database=dotenv_values().get("DB")
    )
    print("Connected to database")
except mariadb.Error as e:
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


@lesd.message_handler(commands=['book'])
def book(message):
    lesdMessages.bookMessage(message)


try:
    lesd.polling()
except Exception as e:
    print(f'Bot error: {e}')
    exit()
