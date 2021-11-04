import string

from mariadb import connection
from telebot import TeleBot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from databaseManager import DatabaseManager


class Messages:
    """Message handler for the bot

    """

    messages = {  # messages that the bot will send for easy access
        'start':
        u'Hola, {name}!, bienvenido al sistema de turnos de eventos de LAG.\n'
        u'Este bot está diseñado para facilitar el uso de los puestos de nuestros eventos mediante el uso de turnos.\n'
        u'Para más información, usa /help',

        'help':
        u'Mis comandos son:\n'
        u'    /new: añade a la base de datos un nuevo puesto empezando por el turno 0.\n'
        u'    /book: añade tu id a la base de datos junto al numero de tu turno. Cuando llegue tu turno se te avisará por este mismo chat.\n'
        u'    /next: pasa al siguiente turno en un puesto.\n'
        u'    /data: manda un mensaje sobre los datos guardados en la base de datos.\n'
        u'    /cancel: cancela tu última cita en un puesto.\n',

        'no_privilege':
        u'No tienes privilegios para ejecutar esta opción.\n',

        'unkown_message':
        u'No puedo entender lo que dices, {name}, si necesitas ayuda puedes probar con /help.',

        'booth_0':
        u'El puesto {booth} ha sido añadido correctamente.',

        'booth_1':
        u'El puesto {booth} ya está en la base de datos.',

        'booth_2':
        u'Error interno en la base de datos, mire el terminal para más informacion',

        'booth_exception':
        u'No se ha encontrado el nombre del puesto en el mensaje, por favor mira la ayuda para ver como utilizar este comando.',

        'book_message':
        u'¿Que puesto quieres reservar?',

        'reserva_bien':
        u'Reserva confirmada para {booth}, cuando sea tu turno se te avisará.\n'
        u'Tu turno es el {turnoUser}, el turno actual es {currentTurn}',

        'reserva_mal':
        u'La reserva no se pudo completar',

        'cancel_message':
        u'¿En qué puesto deseas cancelar tu ultima reserva?',

        'cancel_correct':
        u'Reserva cancelada con éxito',

        'cancel_fail':
        u'La reserva no pudo ser cancelada',

        'next_message':
        u'¿En qué puesto quieres pasar el turno?',

        'nuevo_turno':
        u'Es tu turno para el puesto {booth}',

        'next':
        u'Se ha llamado al turno {shift}',

        'data_stored':
        u'En la base de datos guardo el id de nuestro chat, del cual no se puede sacar ni tu teléfono ni tus datos ya que es un id privado entre tu y yo.\n'
        u'También guardamos la hora a la que reservas y la hora a la que te llamamos por motivos de estadística',

        'no_next':
        u'No hay nadie esperando para el puesto {booth}',

        'enable_message':
        u'¿Qué puesto deseas activar?',

        'booth_enabled':
        u'El puesto {booth} ha sido activado',

        'all_enabled':
        u'Todos los puestos están activados',

        'no_booths':
        u'No hay puestos disponibles',

        'disable_message':
        u'¿Qué puesto desea desactivar',

        'booth_disabled':
        u'El puesto {booth} ha sido desactivado'
    }

    def __init__(self, lesd: TeleBot) -> None:
        """Constructor

        Arguments:
            lesd (telebot.TeleBot): Bot that sends the messages
        """
        self.lesd = lesd

    def sendStartMessage(self, message: types.Message) -> None:
        """Function to send the start message basic information of the bot

        Arguments:
            message (telebot.types.Message): command message
        """
        self.lesd.send_message(message.chat.id, self.messages['start'].format(
            name=message.chat.first_name))

    def sendHelpMessage(self, message: types.Message) -> None:
        """Function to send the help message containing explications of the bot commands

        Arguments:
            message (telebot.types.Message): command message with the arguments
        """
        self.lesd.send_message(message.chat.id, self.messages["help"])

    def addNewBooth(self, message: types.Message, connection: connection) -> None:
        """Function to add new booths to the database

        Arguments:
            message (telebot.types.Message): command message with the arguments
            connection (mariadb.connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        if(dbm.checkAdmin(message.from_user.username)):
            splitMessage = message.text.split()
            # splits the message to get: splitMessage[0] = command & splitMessage[1] = name of the booth
            if(len(splitMessage) != 2):
                # len must be 2
                self.lesd.send_message(
                    message.chat.id, self.messages['booth_exception'])
            else:
                booth = splitMessage[1]
                result = dbm.addBooth(booth.upper())
                if(result == 2):
                    # db error
                    self.lesd.send_message(
                        message.chat.id, self.messages['booth_2'])
                else:
                    # result will be 1 if an error ocurred or 0 if not
                    self.lesd.send_message(
                        message.chat.id, self.messages[f'booth_{result}'].format(booth=booth))
        else:
            # No privilege message
            self.lesd.send_message(
                message.chat.id, self.messages['no_privilege'])

    def messageNotRecogniced(self, message: types.Message) -> None:
        """Message sent when a message is not recogniced

        Args:
            message (telebot.types.Message): unrecogniced message
        """
        self.lesd.send_message(
            message.chat.id, self.messages['unkown_message'].format(name=message.chat.first_name))

    def keyboardGenerator(self, buttonType: string, connection: connection, message: types.Message, enabled: bool = False) -> None:
        """Keyboard generator for the different commands

        Args:
            buttonType (string): name of the command
            connection (connection): connection to the database
            message (types.Message): message sent to the bot
            enabled (bool, optional): If the booth has to be enabled or not. Defaults to False.
        """

        buttons = InlineKeyboardMarkup()
        buttons.row_width = 2

        dbm = DatabaseManager(connection)
        booths = dbm.getBooths(enabled)  # Gets all enabled booths
        if(len(booths) == 0):
            # No booths in list
            self.lesd.send_message(message.chat.id, self.messages['no_booths'])
        else:
            for booth in booths:
                (name, ) = booth
                # adds the name of the booth to the keyboard
                buttons.add(InlineKeyboardButton(
                    name, callback_data=buttonType+name))

            self.lesd.send_message(
                message.chat.id, self.messages[buttonType+'message'], reply_markup=buttons)

    def booking(self, booth: string, message: types.Message, connection: connection) -> None:
        """Booking method to add a new book to the database

        Args:
            booth (string): name of the booth
            message (types.Message): message sent from the bot
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        (result, userTurn, currentTurn) = dbm.addBook(message.chat.id, booth)
        if(result == 0):
            self.lesd.send_message(
                message.chat.id, self.messages['reserva_bien'].format(booth=booth, currentTurn=currentTurn, turnoUser=userTurn))
        else:
            self.lesd.send_message(
                message.chat.id, self.messages['reserva_mal'])

        self.lesd.delete_message(
            message_id=message.message_id, chat_id=message.chat.id)

    def cancel(self, booth: string, message: types.Message, connection: connection) -> None:
        """[summary]

        Args:
            booth (string): [booth name]
            message (types.Message): [message sent by the bot]
            connection (connection): [connection to the database]
        """
        dbm = DatabaseManager(connection)
        if(dbm.cancelLast(message.chat.id, booth)):
            self.lesd.send_message(
                message.chat.id, self.messages['cancel_correct'])
        else:
            self.lesd.send_message(
                message.chat.id, self.messages['cancel_fail'])
        self.lesd.delete_message(
            message_id=message.message_id, chat_id=message.chat.id)

    def next(self, booth: string, message: types.Message, connection: connection) -> None:
        """Sends a warning message for the next person in a booth

        Args:
            booth (string): name of the booth
            message (types.Message): message with the buttons
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        (nextUserID, shift) = dbm.callNext(booth)
        if(nextUserID != 0):
            if(nextUserID == 1):
                self.lesd.send_message(
                    message.message_id, self.messages['no_next'].format(booth=booth))
            # Message to next user
            self.lesd.send_message(
                nextUserID, self.messages['nuevo_turno'].format(booth=booth))
            # Message to admin
            self.lesd.send_message(
                message.chat.id, self.messages['next'].format(shift=shift))
            self.lesd.delete_message(
                message_id=message.message_id, chat_id=message.chat.id)

    def dataMessage(self, message: types.Message):
        """Message sent explained the stored data

        Args:
            message (types.Message): message sent to the bot
        """
        self.lesd.send_message(message.chat.id, self.messages['data_stored'])

    def enableEvent(self, booth: string, message: types.Message, connection: connection):
        """Event enabler

        Args:
            booth (string): name of the booth
            message (types.Message): message sent to the bot
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        dbm.enableEvent(booth)
        self.lesd.send_message(
            message.chat.id, self.messages['booth_enabled'].format(booth=booth))
        self.lesd.delete_message(
            message_id=message.message_id, chat_id=message.chat.id)

    def disableEvent(self, booth: string, message: types.Message, connection: connection):
        """Event disabler

        Args:
            booth (string): name of the booth
            message (types.Message): message sent to the bot
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        dbm.disableEvent(booth)
        self.lesd.send_message(
            message.chat.id, self.messages['booth_disabled'].format(booth=booth))
        self.lesd.delete_message(
            message_id=message.message_id, chat_id=message.chat.id)
