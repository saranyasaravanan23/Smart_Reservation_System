
from mysql.connector import Error


class WaitingList:

    @staticmethod
    def view_waiting_list(connection):
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    w.waiting_id,
                    p.passenger_name,
                    p.email,
                    b.bus_number,
                    w.booking_status,
                    w.waiting_date
                FROM waiting_list w
                JOIN passengers p
                    ON w.passenger_id = p.passenger_id
                JOIN buses b
                    ON w.bus_id = b.bus_id
                ORDER BY w.waiting_date, w.waiting_id
            """)

            records = cursor.fetchall()

            print("\n===== WAITING LIST =====")

            if not records:
                print("Waiting list is empty.")
                return

            for record in records:
                print("\nWaiting ID:", record["waiting_id"])
                print("Passenger:", record["passenger_name"])
                print("Email:", record["email"])
                print("Bus Number:", record["bus_number"])
                print("Status:", record["booking_status"])
                print("Waiting Date:", record["waiting_date"])

        except Error as error:
            print("Database Error:", error)
        finally:
            cursor.close()
