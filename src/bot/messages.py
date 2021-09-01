import mariadb
import telebot

from databaseManager import DatabaseManager


class Messages:
    """Message handler for the bot

    """

    def __init__(self, lesd: telebot.TeleBot) -> None:
        """Constructor

        Arguments:
            lesd (telebot.TeleBot): Bot that sends the messages
        """
        self.lesd = lesd

    def sendStartMessage(self, message: telebot.types.Message) -> None:
        """Function to send the start message basic information of the bot

        Arguments:
            message (telebot.types.Message): command message
        """

        self.lesd.send_message(message.chat.id, """Bienvenido al sistema de turnos de eventos de LAG
        · Para añadir un nuevo puesto usa el comando /new
        · Para pedir turno en un puesto usa el comando /book
        · Para pasar el turno en un evento usa el comando /next seguido del nombre del puesto""")

    def sendHelpMessage(self, message: telebot.types.Message) -> None:
        """Function to send the help message containing explications of the bot commands

        Arguments:
            message (telebot.types.Message): command message with the arguments
        """
        self.lesd.send_message(message.chat.id, """Mis comandos son:
        /new : añade a la base de datos un nuevo puesto empezando por el turno 0
        /book: añade tu id a la base de datos junto al numero de tu turno. Cuando llegue tu turno se te avisará por este mismo chat.
        /next <nombre del puesto>: pasa al siguiente turno en un puesto""")

    def addNewBooth(self, message: telebot.types.Message, connection: mariadb.connection) -> None:
        """Function to add new booths to the database

        Arguments:
            message (telebot.types.Message): command message with the arguments
            connection (mariadb.connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        if(dbm.checkAdmin(message.from_user.username)):
            splitMessage = message.text.split()
            if(len(splitMessage) != 2):
                self.lesd.send_message(
                    message.chat.id, "No se ha encontrado el nombre del puesto en el mensaje, por favor mira la ayuda para ver como utilizar este comando.")
            else:

                self.lesd.send_message(message.chat.id, {
                    0: "Puesto añadido correctamente",
                    1: "Puesto ya en la base de datos",
                    2: "Error interno en la base de datos, mire el terminal para más informacion",
                }[dbm.addBooth(splitMessage[1].upper())])
        else:
            self.lesd.send_message(
                message.chat.id, "No tienes privilegios para ejecutar esta opción")
