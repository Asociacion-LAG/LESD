import string

import mariadb


class DatabaseManager(object):

    def __init__(self, connection: mariadb.connection):
        self.connection = connection

    @classmethod
    def checkAdmin(self, user: string) -> bool:
        self.connection.execute(
            "SELECT count(*) from Admin where username =?", (user,))
        if(self.connection != 0):
            return True
        else:
            return False
