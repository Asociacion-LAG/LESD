import string
from typing import List, Tuple

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
        if(result == 1):
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
        if(self.checkIfBoothIsValid(booth) == False):
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

    def addBook(self, user: string, booth: string) -> Tuple[int, int, int]:
        """Adds a booking to the database

        Args:
            user(string): user chat ID
            booth(string): name of the booth

        Returns:
            Tuple[int, int, int]: first one is a code error, second one user turn, last one current turn
        """
        if(self.checkIfBoothIsValid(booth)):
            try:
                self.cursor.execute(
                    'SELECT COUNT(*) FROM bookings where booth=?', (booth,))
                (lastNum,) = self.cursor.fetchone()
                self.cursor.execute(
                    'INSERT INTO bookings (booth, userId, shift, bookTime) Value (?,?,?, CURRENT_TIME)', (booth, user, lastNum + 1, ))
                self.connection.commit()
                self.cursor.execute(
                    'Select currentShift from booths where booth=?', (booth,))
                (currentShift,) = self.cursor.fetchone()
                return (0, lastNum + 1, currentShift)
            except Error as e:
                print(f"[DB ERROR]: {e}")
                return 2
        else:
            return 1

    def getBooths(self, enabled: bool = False) -> list:
        """Returns all Booths in the database

        Args:
            enabled (bool, optional): if the booth has to be enabled or not. Defaults to False.

        Returns:
            [list]: list with all the booths selected
        """
        if(enabled):
            self.cursor.execute('SELECT booth FROM Booths WHERE enabled=1')
        else:
            self.cursor.execute('SELECT Booth FROM Booths WHERE enabled=0')
        return self.cursor.fetchall()

    def cancelLast(self, id: string, booth: string) -> bool:
        """Cancel last book from a user

        Args:
            id (string): id between the user and the bot
            booth (string): name of the booth

        Returns:
            bool: [description]
        """
        try:
            self.cursor.execute(
                'Select `shift` from bookings where userID=? AND booth=? order by shift desc', (id, booth, ))
            (shift,) = self.cursor.fetchone()

            self.cursor.execute(
                'Update bookings set canceled=1 where userID=? and booth=? and shift=?', (id, booth, shift, ))

            self.connection.commit()
            return True
        except Exception as e:
            return False

    def callNext(self, booth: string) -> Tuple[int, int]:
        """Get next user id on the list and the current shift.

        Args:
            booth (string): name of the booth

        Returns:
            Tuple[int, int]: (userId, shift of the user)
        """
        try:
            # Get current shift
            self.cursor.execute(
                'SELECT currentShift from booths where booth=?', (booth, ))
            (currentShift,) = self.cursor.fetchone()

            # Update current shift
            self.cursor.execute(
                'SELECT COUNT(*) from bookings where booth=? and shift >?', (booth, currentShift))
            (resul,) = self.cursor.fetchone()
            if(resul != 0):
                # Current shift update
                self.cursor.execute(
                    'UPDATE booths set currentShift = currentShift + 1 where booth=?', (booth,))

                self.cursor.execute(
                    'Select currentShift from booths where booth=?', (booth,))
                (currentShift, ) = self.cursor.fetchone()
                # Select next user id
                self.cursor.execute(
                    'SELECT userID, canceled from bookings where booth=? and shift=?', (booth, currentShift, ))

                (userID, canceled, ) = self.cursor.fetchone()
                # Update time where user is called
                self.cursor.execute(
                    'Update bookings set enterTime = CURRENT_TIME where booth=? and userID=?', (booth, userID, ))

                self.connection.commit()
                if(canceled == 1):
                    return self.callNext(booth)
                else:
                    return userID, currentShift
            else:
                return 1, 0
        except Exception as e:
            print(f"DB Error: {e}")
            return 0, 0

    def enableEvent(self, booth: string) -> None:
        """Enable a event in the database

        Args:
            booth (string): name of the booth
        """
        try:
            self.cursor.execute(
                'UPDATE booths set enabled = 1 where booth=?', (booth,))
            self.connection.commit()
        except Exception as e:
            print(f"DB Error: {e}")

    def disableEvent(self, booth: string) -> None:
        """Disable a event in the database

        Args:
            booth (string): name of the booth
        """
        try:
            self.cursor.execute(
                'UPDATE booths set enabled = 0 where booth=?', (booth,))
            self.connection.commit()
        except Exception as e:
            print(f"DB Error: {e}")
