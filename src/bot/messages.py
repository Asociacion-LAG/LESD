import mariadb
import telebot

from databaseManager import DatabaseManager


class Messages:
    """Message handler for the bot

    """

    messages = {
        'start':
        u'Hola, {name}!, bienvenido al sistema de turnos de eventos de LAG.\n'
        u'Este bot está diseñado para facilitar el uso de los puestos de nuestros eventos mediante el uso de turnos.\n'
        u'Para más información, usa /help',

        'help':
        u'Mis comandos son:\n'
        u'    /new: añade a la base de datos un nuevo puesto empezando por el turno 0.\n'
        u'    /book: añade tu id a la base de datos junto al numero de tu turno. Cuando llegue tu turno se te avisará por este mismo chat.\n'
        u'    /next < nombre del puesto >: pasa al siguiente turno en un puesto.',

        'no_privilege':
        u'No tienes privilegios para ejecutar esta opción.\n',

        'unkown_message':
        u'No puedo entender lo que dices, {name}, si necesitas ayuda puedes probar con /help.',

        'boot_0':
        u'El puesto {booth} ha sido añadido correctamente.',

        'booth_1':
        u'El puesto {booth} ya está en la base de datos.',

        'booth_2':
        u'Error interno en la base de datos, mire el terminal para más informacion',

        'booth_exception':
        u'No se ha encontrado el nombre del puesto en el mensaje, por favor mira la ayuda para ver como utilizar este comando.',
    }

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

        self.lesd.send_message(message.chat.id, self.messages['start'].format(
            name=message.chat.first_name))

    def sendHelpMessage(self, message: telebot.types.Message) -> None:
        """Function to send the help message containing explications of the bot commands

        Arguments:
            message (telebot.types.Message): command message with the arguments
        """
        self.lesd.send_message(message.chat.id, self.messages["help"])

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
                    message.chat.id, self.messages['booth_exception'])
            else:

                self.lesd.send_message(message.chat.id, {
                    0: self.messages['boot_0'.format(booth=splitMessage[1])],
                    1: self.messages['boot_1'.format(booth=splitMessage[1])],
                    2: self.messages['booth_2'],
                }[dbm.addBooth(splitMessage[1].upper())])
        else:
            self.lesd.send_message(
                message.chat.id, self.messages['no_privilege'])

    def messageNotRecogniced(self, message: telebot.types.Message) -> None:
        """Message sent when a message is not recogniced

        Args:
            message (telebot.types.Message): unrecogniced message
        """
        self.lesd.send_message(
            message.chat.id, self.messages['unkown_message'].format(name=message.chat.first_name))
