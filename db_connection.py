
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="api_user",
            password="ApiUser12345",
            database="user_management_db"
        )

        if connection.is_connected():
            print("MySQL Database Connected Successfully!")
            return connection

    except Error as error:
        print("Database Connection Error:", error)

    return None


if __name__ == "__main__":
    connection = get_connection()

    if connection:
        connection.close()
