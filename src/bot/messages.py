import telebot

from databaseManager import DatabaseManager


class Messages(object):

    def __init__(self, lesd: telebot.TeleBot):
        self.lesd = lesd

    @classmethod
    def sendStartMessage(self, message):
        self.lesd.send_message(message.chat.id, """Bienvenido al sistema de turnos de eventos de LAG 
        · Para añadir un nuevo puesto usa el comando /new 
        · Para pedir turno en un puesto usa el comando /book
        · Para pasar el turno en un evento usa el comando /next seguido del nombre del puesto""")

    @classmethod
    def sendHelpMessage(self, message):
        self.lesd.send_message(message.chat.id, """Mis comandos son:
        /new : añade a la base de datos un nuevo puesto empezando por el turno 0
        /book: añade tu id a la base de datos junto al numero de tu turno. Cuando llegue tu turno se te avisará por este mismo chat.
        /next <nombre del puesto>: pasa al siguiente turno en un puesto""")

    @classmethod
    def addNewBooth(self, message, connection):
        dbm = DatabaseManager(connection)
        if(dbm.checkAdmin(message.from_user.username)):
            print(True)
