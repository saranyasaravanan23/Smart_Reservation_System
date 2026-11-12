
from mysql.connector import Error, IntegrityError


class Bus:

    def __init__(self, bus_id, bus_number, route_id, total_seats):
        self.bus_id = bus_id
        self.bus_number = bus_number
        self.route_id = route_id
        self.total_seats = total_seats

    def display_bus(self):
        print("\n===== BUS DETAILS =====")
        print("Bus ID:", self.bus_id)
        print("Bus Number:", self.bus_number)
        print("Route ID:", self.route_id)
        print("Total Seats:", self.total_seats)

    # 1. Add New Bus
    @staticmethod
    def add_bus(connection):

        cursor = connection.cursor()

        try:
            print("\n===== ADD NEW BUS =====")

            bus_number = input("Enter Bus Number: ").strip()
            source = input("Enter Source: ").strip()
            destination = input("Enter Destination: ").strip()
            departure = input("Enter Departure Time (HH:MM:SS): ").strip()
            arrival = input("Enter Arrival Time (HH:MM:SS): ").strip()

            ticket_price = float(input("Enter Ticket Price: "))
            total_seats = int(input("Enter Total Seats: "))

            if not all([bus_number, source, destination, departure, arrival]):
                raise ValueError("All bus details are required.")

            if source.lower() == destination.lower():
                raise ValueError("Source and destination cannot be the same.")

            if ticket_price <= 0 or total_seats <= 0:
                raise ValueError("Price and seat capacity must be positive.")

            # Finish any previous read transaction before starting a new one
            if connection.in_transaction:
                connection.rollback()

            connection.start_transaction()

            # Insert route details
            route_query = """
                INSERT INTO routes
                (source, destination, departure_time,
                 arrival_time, ticket_price)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                route_query,
                (source, destination, departure, arrival, ticket_price)
            )

            route_id = cursor.lastrowid

            # Insert bus details
            bus_query = """
                INSERT INTO buses
                (bus_number, route_id, total_seats)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                bus_query,
                (bus_number, route_id, total_seats)
            )

            bus_id = cursor.lastrowid

            # Automatically create seats
            seat_query = """
                INSERT INTO seats (bus_id, seat_number)
                VALUES (%s, %s)
            """

            for seat_number in range(1, total_seats + 1):
                cursor.execute(
                    seat_query,
                    (bus_id, seat_number)
                )

            # Save all changes
            connection.commit()

            print("\nBus Added Successfully!")
            print("Bus ID:", bus_id)
            print("Route ID:", route_id)
            print("Total Seats Created:", total_seats)

        except ValueError as error:
            connection.rollback()
            print("Invalid Input:", error)

        except IntegrityError as error:
            connection.rollback()
            print("Duplicate or Database Constraint Error:", error)

        except Error as error:
            connection.rollback()
            print("Database Error:", error)

        finally:
            cursor.close()

    # 2. View Available Buses
    @staticmethod
    def view_available_buses(connection):

        cursor = connection.cursor(dictionary=True)

        try:
            query = """
                SELECT
                    b.bus_id,
                    b.bus_number,
                    r.source,
                    r.destination,
                    r.departure_time,
                    r.arrival_time,
                    r.ticket_price,
                    b.total_seats,
                    SUM(
                        CASE
                            WHEN s.seat_status = 'AVAILABLE'
                            THEN 1 ELSE 0
                        END
                    ) AS available_seats
                FROM buses b
                JOIN routes r ON b.route_id = r.route_id
                LEFT JOIN seats s ON b.bus_id = s.bus_id
                GROUP BY
                    b.bus_id,
                    b.bus_number,
                    r.source,
                    r.destination,
                    r.departure_time,
                    r.arrival_time,
                    r.ticket_price,
                    b.total_seats
            """

            cursor.execute(query)
            buses = cursor.fetchall()

            print("\n===== AVAILABLE BUSES =====")

            if not buses:
                print("No buses found.")
                return

            for bus in buses:
                print("\nBus ID:", bus["bus_id"])
                print("Bus Number:", bus["bus_number"])
                print("Source:", bus["source"])
                print("Destination:", bus["destination"])
                print("Departure:", bus["departure_time"])
                print("Arrival:", bus["arrival_time"])
                print("Ticket Price:", bus["ticket_price"])
                print("Total Seats:", bus["total_seats"])
                print("Available Seats:", bus["available_seats"])

        except Error as error:
            print("Database Error:", error)

        finally:
            cursor.close()

    # 3. Search Buses
    @staticmethod
    def search_buses(connection):

        cursor = connection.cursor(dictionary=True)

        try:
            print("\n===== SEARCH BUSES =====")

            source = input("Enter Source: ").strip()
            destination = input("Enter Destination: ").strip()

            if not source or not destination:
                raise ValueError(
                    "Source and destination are required."
                )

            query = """
                SELECT
                    b.bus_id,
                    b.bus_number,
                    r.source,
                    r.destination,
                    r.departure_time,
                    r.arrival_time,
                    r.ticket_price,
                    b.total_seats,
                    SUM(
                        CASE
                            WHEN s.seat_status = 'AVAILABLE'
                            THEN 1 ELSE 0
                        END
                    ) AS available_seats
                FROM buses b
                JOIN routes r ON b.route_id = r.route_id
                LEFT JOIN seats s ON b.bus_id = s.bus_id
                WHERE LOWER(r.source) = LOWER(%s)
                AND LOWER(r.destination) = LOWER(%s)
                GROUP BY
                    b.bus_id,
                    b.bus_number,
                    r.source,
                    r.destination,
                    r.departure_time,
                    r.arrival_time,
                    r.ticket_price,
                    b.total_seats
            """

            cursor.execute(query, (source, destination))
            buses = cursor.fetchall()

            if not buses:
                print("No buses found for this route.")
                return

            print("\n===== SEARCH RESULTS =====")

            for bus in buses:
                print("\nBus ID:", bus["bus_id"])
                print("Bus Number:", bus["bus_number"])
                print("Source:", bus["source"])
                print("Destination:", bus["destination"])
                print("Departure:", bus["departure_time"])
                print("Arrival:", bus["arrival_time"])
                print("Ticket Price: Rs.", bus["ticket_price"])
                print("Total Seats:", bus["total_seats"])
                print("Available Seats:", bus["available_seats"])

        except ValueError as error:
            print("Invalid Input:", error)

        except Error as error:
            print("Database Error:", error)

        finally:
            cursor.close()
