import string

from mariadb import connection
from telebot import TeleBot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

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
        u'    /next < nombre del puesto >: pasa al siguiente turno en un puesto.'
        u'    /data: manda un mensaje sobre los datos guardados en la base de datos.',

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
        u'Reserva confirmada para {booth}, cuando sea tu turno se te avisará',

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

        'data_stored':
        u'En la base de datos guardo el id de nuestro chat, del cual no se puede sacar ni tu teléfono ni tus datos ya que es un id privado entre tu y yo.'
        u'También guardamos la hora a la que reservas y la hora a la que te llamamos por motivos de estadística'
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
            if(len(splitMessage) != 2):
                self.lesd.send_message(
                    message.chat.id, self.messages['booth_exception'])
            else:
                booth = splitMessage[1]
                result = dbm.addBooth(booth.upper())
                if(result == 2):
                    self.lesd.send_message(
                        message.chat.id, self.messages['booth_2'])
                else:
                    self.lesd.send_message(
                        message.chat.id, self.messages['booth_0'.format(booth)])
        else:
            self.lesd.send_message(
                message.chat.id, self.messages['no_privilege'])

    def messageNotRecogniced(self, message: types.Message) -> None:
        """Message sent when a message is not recogniced

        Args:
            message (telebot.types.Message): unrecogniced message
        """
        self.lesd.send_message(
            message.chat.id, self.messages['unkown_message'].format(name=message.chat.first_name))

    def bookMessage(self, message: types.Message, conn:  connection) -> None:
        """Booking message to display the buttons for each booth

        Args:
            message (types.Message): message sent to the bot
            conn (connection): connection to the database
        """
        buttons = InlineKeyboardMarkup()
        buttons.row_width = 1

        dbm = DatabaseManager(conn)
        booths = dbm.getBooths()

        for booth in booths:
            (name, ) = booth
            buttons.add(InlineKeyboardButton(
                name, callback_data=f"book_{name}"))

        self.lesd.send_message(
            message.chat.id, self.messages['book_message'], reply_markup=buttons)

    def booking(self, booth: string, message: types.Message, connection: connection) -> None:
        """Booking method to add a new book to the database

        Args:
            booth (string): name of the booth
            message (types.Message): message sent from the bot
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        result = dbm.addBook(message.chat.id, booth)
        if(result == 0):
            self.lesd.send_message(
                message.chat.id, self.messages['reserva_bien'].format(booth=booth))
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

    def cancelMessage(self, message: types.Message, conn: connection) -> None:
        """Cancel message to display the buttons for each booth

        Args:
            message (types.Message): message sent to the bot
            conn (connection): connection to the database
        """
        buttons = InlineKeyboardMarkup()
        buttons.row_width = 1

        dbm = DatabaseManager(conn)
        booths = dbm.getBooths()

        for booth in booths:
            (name, ) = booth
            buttons.add(InlineKeyboardButton(
                name, callback_data=f"cancel_{name}"))

        self.lesd.send_message(
            message.chat.id, self.messages['cancel_message'], reply_markup=buttons)

    def nextMessage(self, message: types.Message, conn: connection) -> None:
        """Next message to display the buttons for each booth

        Args:
            message (types.Message): message sent to the bot
            conn (connection): connection to the database
        """
        buttons = InlineKeyboardMarkup()
        buttons.row_width = 1

        dbm = DatabaseManager(conn)
        booths = dbm.getBooths()

        for booth in booths:
            (name, ) = booth
            buttons.add(InlineKeyboardButton(
                name, callback_data=f"next_{name}"))

        self.lesd.send_message(
            message.chat.id, self.messages['next_message'], reply_markup=buttons)

    def next(self, booth: string, message: types.Message, connection: connection) -> None:
        """Sends a warning message for the next person in a booth

        Args:
            booth (string): name of the booth
            message (types.Message): message with the buttons
            connection (connection): connection to the database
        """
        dbm = DatabaseManager(connection)
        nextUserID = dbm.callNext(booth)
        if(nextUserID != 0):
            self.lesd.send_message(
                nextUserID, self.messages['nuevo_turno'].format(booth=booth))
            self.lesd.delete_message(
                message_id=message.message_id, chat_id=message.chat.id)

    def dataMessage(self, message: types.Message):
        """Message sent explained the stored data

        Args:
            message (types.Message): message sent to the bot
        """
        self.lesd.send_message(message.chat.id, self.messages['data_stored'])
