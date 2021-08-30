
import string
from os import system

import mariadb
import telebot
from dotenv import load_dotenv
from dotenv.main import dotenv_values

import databaseManager
import messages

load_dotenv()


lesd = telebot.TeleBot(dotenv_values().get("TOKEN"))

lesdMessages = messages.Messages(lesd)
print(dotenv_values().get("DB_USER"))
try:
    connection = mariadb.connect(
        user=dotenv_values().get("DB_USER"),
        password=dotenv_values().get("DB_PSSW"),
        host="raspi-3",
        database="LAG_Events"
    )
except mariadb.Error as e:
    print(f"Error: {e}")


# COMMAND HANDLERS

@lesd.message_handler(commands=['start'])
def start(message):
    lesdMessages.sendStartMessage(message)


@lesd.message_handler(commands=['help'])
def help(message):
    lesdMessages.sendHelpMessage(message)


@lesd.message_handler(commands=['new'])
def new(message):
    lesd.addNewBooth(message, connection)


lesd.polling()
