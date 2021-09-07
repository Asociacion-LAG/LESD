import string

from mariadb import Error, connection


class DatabaseManager:
    """Database manager for the bot
    """

    def __init__(self, connection: connection) -> None:
        """Constructor

        Args:
            connection (mariadb.connection): Connection to the database
        """
        self.connection = connection
        # Storaged cursor for the execution of queries
        self.cursor = self.connection.cursor()

    def checkAdmin(self, user: string) -> bool:
        """Checks if the user that sent the message is an admin

        Args:
            user (string): telegram username of the sender of the message

        Returns:
            bool: True if the user is admin, false otherwise
        """
        self.cursor.execute(
            "SELECT count(*) from LAG_Events.Admins where username =?", (user,))
        (result,) = self.cursor.fetchone()  # Number stored in cursor
        if(result != 0):
            return True
        else:
            return False

    def checkIfBoothIsValid(self, booth: string) -> bool:
        """Checks if a booth is on the database

        Args:
            booth (string): name of the booth

        Returns:
            bool: True if the booth is on the database, false otherwise
        """
        self.cursor.execute(
            "Select count(*) from Booths where booth =?", (booth,))
        (result,) = self.cursor.fetchone()  # Number stored in cursor
        if(result == 0):
            return True
        else:
            return False

    def addBooth(self, booth: string) -> int:
        """Adds a new booth to the database

        Args:
            booth (string): name of the booth, put its current shift to 0 by default

        Returns:
            int: 0 if the query executed correctly, 1 if the booth was already on the database and 2 if there was an SQL error
        """
        if(self.checkIfBoothIsValid(booth)):
            try:
                self.cursor.execute(
                    "Insert into Booths (booth) value (?)", (booth,))  # Add booth
                self.connection.commit()  # Commit changes to database
                return 0
            except Error as e:
                print(f"[DB ERROR]: {e}")
                return 2
        else:
            return 1

    def addBook(self, user: string, booth: string) -> int:
        """Adds a booking to the database

        Args:
            user (string): user chat ID
            booth (string): name of the booth

        Returns:
            int: 0 if everything went OK, 1 if the booth was not in de database, 2 if an error ocurred
        """
        if(self.checkIfBoothIsValid(booth)):
            try:
                self.cursor.execute(
                    'SELECT COUNT(*) FROM bookings where booth=?', (booth))
                (lastNum,) = self.cursor.fetchone()
                self.cursor.execute(
                    'INSERT INTO bookings (booth, userId, shift) Value (?,?,?)', (booth, user, lastNum + 1))
                self.connection.commit()
                return 0
            except Error as e:
                print(f"[DB ERROR]: {e}")
                return 2
        else:
            return 1
