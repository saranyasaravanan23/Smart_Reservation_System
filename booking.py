
from mysql.connector import Error, IntegrityError


class Booking:

    # 1. View Available Seats
    @staticmethod
    def view_available_seats(connection, bus_id):
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute("""
                SELECT seat_number, seat_status
                FROM seats
                WHERE bus_id = %s
                ORDER BY seat_number
            """, (bus_id,))

            seats = cursor.fetchall()

            print("\n===== SEAT AVAILABILITY =====")

            if not seats:
                print("No seats found for this bus.")
                return

            for seat in seats:
                print(
                    "Seat:", seat["seat_number"],
                    "| Status:", seat["seat_status"]
                )

        except Error as error:
            print("Database Error:", error)

        finally:
            cursor.close()

    # 2. Book Ticket
    @staticmethod
    def book_ticket(connection):
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            print("\n===== BOOK BUS TICKET =====")

            name = input("Enter Passenger Name: ").strip()
            email = input("Enter Email: ").strip()
            phone = input("Enter Phone Number: ").strip()
            bus_id = int(input("Enter Bus ID: "))

            if not name or not email or not phone:
                raise ValueError("All passenger details are required.")

            if "@" not in email or "." not in email:
                raise ValueError("Invalid email address.")

            if not phone.isdigit() or not 10 <= len(phone) <= 15:
                raise ValueError("Invalid phone number.")

            if bus_id <= 0:
                raise ValueError("Invalid Bus ID.")

            # Clear any previous unfinished transaction
            if connection.in_transaction:
                connection.rollback()

            connection.start_transaction()

            # Lock bus record
            cursor.execute("""
                SELECT bus_id
                FROM buses
                WHERE bus_id = %s
                FOR UPDATE
            """, (bus_id,))

            if not cursor.fetchone():
                raise ValueError("Bus ID not found.")

            # Check passenger
            cursor.execute("""
                SELECT passenger_id, passenger_name, phone
                FROM passengers
                WHERE email = %s
            """, (email,))

            passenger = cursor.fetchone()

            if passenger:
                if (
                    passenger["passenger_name"] != name
                    or passenger["phone"] != phone
                ):
                    raise ValueError(
                        "Email already belongs to another passenger."
                    )

                passenger_id = passenger["passenger_id"]

            else:
                cursor.execute("""
                    SELECT passenger_id
                    FROM passengers
                    WHERE phone = %s
                """, (phone,))

                if cursor.fetchone():
                    raise ValueError("Phone number already exists.")

                cursor.execute("""
                    INSERT INTO passengers
                    (passenger_name, email, phone)
                    VALUES (%s, %s, %s)
                """, (name, email, phone))

                passenger_id = cursor.lastrowid

            # Prevent duplicate confirmed booking
            cursor.execute("""
                SELECT booking_id
                FROM bookings
                WHERE passenger_id = %s
                AND bus_id = %s
                AND booking_status = 'CONFIRMED'
            """, (passenger_id, bus_id))

            if cursor.fetchone():
                raise ValueError(
                    "Passenger already has a confirmed ticket on this bus."
                )

            # Check available seats
            cursor.execute("""
                SELECT seat_id, seat_number
                FROM seats
                WHERE bus_id = %s
                AND seat_status = 'AVAILABLE'
                ORDER BY seat_number
                FOR UPDATE
            """, (bus_id,))

            available_seat = cursor.fetchone()

            # If bus is full, add passenger to waiting list
            if not available_seat:

                cursor.execute("""
                    SELECT waiting_id
                    FROM waiting_list
                    WHERE passenger_id = %s
                    AND bus_id = %s
                    AND booking_status = 'WAITING'
                """, (passenger_id, bus_id))

                if cursor.fetchone():
                    raise ValueError(
                        "Passenger is already in the waiting list."
                    )

                cursor.execute("""
                    INSERT INTO waiting_list
                    (passenger_id, bus_id, booking_status)
                    VALUES (%s, %s, 'WAITING')
                """, (passenger_id, bus_id))

                waiting_id = cursor.lastrowid
                connection.commit()

                print("\nBus is FULL.")
                print("Passenger added to waiting list.")
                print("Waiting ID:", waiting_id)
                print("Waiting Status: WAITING")
                return

            # Ask user to select seat
            print("\nAvailable seat found.")

            seat_number = int(input("Enter Seat Number: "))

            cursor.execute("""
                SELECT seat_id, seat_status
                FROM seats
                WHERE bus_id = %s
                AND seat_number = %s
                FOR UPDATE
            """, (bus_id, seat_number))

            seat = cursor.fetchone()

            if not seat:
                raise ValueError("Invalid seat number.")

            if seat["seat_status"] != "AVAILABLE":
                raise ValueError("This seat is already booked.")

            # Get ticket price
            cursor.execute("""
                SELECT r.ticket_price
                FROM buses b
                JOIN routes r ON b.route_id = r.route_id
                WHERE b.bus_id = %s
            """, (bus_id,))

            route = cursor.fetchone()

            if not route:
                raise ValueError("Bus route not found.")

            # Update seat status
            cursor.execute("""
                UPDATE seats
                SET seat_status = 'BOOKED'
                WHERE seat_id = %s
                AND seat_status = 'AVAILABLE'
            """, (seat["seat_id"],))

            if cursor.rowcount != 1:
                raise ValueError("Seat is already booked.")

            # Insert booking
            cursor.execute("""
                INSERT INTO bookings
                (passenger_id, bus_id, seat_id, total_amount)
                VALUES (%s, %s, %s, %s)
            """, (
                passenger_id,
                bus_id,
                seat["seat_id"],
                route["ticket_price"]
            ))

            booking_id = cursor.lastrowid

            connection.commit()

            print("\n===== BOOKING CONFIRMED =====")
            print("Booking ID:", booking_id)
            print("Passenger:", name)
            print("Bus ID:", bus_id)
            print("Seat Number:", seat_number)
            print("Ticket Amount: Rs.", route["ticket_price"])
            print("Status: CONFIRMED")
            print("Ticket Booked Successfully!")

        except ValueError as error:
            connection.rollback()
            print("Booking Error:", error)

        except IntegrityError as error:
            connection.rollback()
            print("Duplicate or Constraint Error:", error)

        except Error as error:
            connection.rollback()
            print("Database Error:", error)

        finally:
            cursor.close()

    # 3. Cancel Ticket
    @staticmethod
    def cancel_ticket(connection):
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            print("\n===== CANCEL TICKET =====")

            booking_id = int(input("Enter Booking ID: "))

            if connection.in_transaction:
                connection.rollback()

            connection.start_transaction()

            cursor.execute("""
                SELECT booking_id, passenger_id, bus_id,
                       seat_id, booking_status
                FROM bookings
                WHERE booking_id = %s
                FOR UPDATE
            """, (booking_id,))

            booking = cursor.fetchone()

            if not booking:
                raise ValueError("Booking ID not found.")

            if booking["booking_status"] != "CONFIRMED":
                raise ValueError("This ticket is already cancelled.")

            # Cancel booking
            cursor.execute("""
                UPDATE bookings
                SET booking_status = 'CANCELLED'
                WHERE booking_id = %s
            """, (booking_id,))

            # Release seat
            cursor.execute("""
                UPDATE seats
                SET seat_status = 'AVAILABLE'
                WHERE seat_id = %s
            """, (booking["seat_id"],))

            # Find oldest waiting passenger
            cursor.execute("""
                SELECT waiting_id, passenger_id
                FROM waiting_list
                WHERE bus_id = %s
                AND booking_status = 'WAITING'
                ORDER BY waiting_date, waiting_id
                LIMIT 1
                FOR UPDATE
            """, (booking["bus_id"],))

            waiting = cursor.fetchone()

            if waiting:

                cursor.execute("""
                    SELECT r.ticket_price
                    FROM buses b
                    JOIN routes r ON b.route_id = r.route_id
                    WHERE b.bus_id = %s
                """, (booking["bus_id"],))

                route = cursor.fetchone()

                # Allocate released seat
                cursor.execute("""
                    UPDATE seats
                    SET seat_status = 'BOOKED'
                    WHERE seat_id = %s
                """, (booking["seat_id"],))

                cursor.execute("""
                    INSERT INTO bookings
                    (passenger_id, bus_id, seat_id, total_amount)
                    VALUES (%s, %s, %s, %s)
                """, (
                    waiting["passenger_id"],
                    booking["bus_id"],
                    booking["seat_id"],
                    route["ticket_price"]
                ))

                new_booking_id = cursor.lastrowid

                cursor.execute("""
                    UPDATE waiting_list
                    SET booking_status = 'ALLOCATED'
                    WHERE waiting_id = %s
                """, (waiting["waiting_id"],))

                print("\nWaiting passenger automatically allocated.")
                print("New Booking ID:", new_booking_id)

            connection.commit()

            print("\nTicket Cancelled Successfully!")

        except ValueError as error:
            connection.rollback()
            print("Cancellation Error:", error)

        except Error as error:
            connection.rollback()
            print("Database Error:", error)

        finally:
            cursor.close()

    # 4. View Booking History
    @staticmethod
    def view_booking_history(connection):
        cursor = connection.cursor(dictionary=True, buffered=True)

        try:
            cursor.execute("""
                SELECT
                    b.booking_id,
                    p.passenger_name,
                    bu.bus_number,
                    s.seat_number,
                    b.booking_date,
                    b.total_amount,
                    b.booking_status
                FROM bookings b
                JOIN passengers p
                    ON b.passenger_id = p.passenger_id
                JOIN buses bu
                    ON b.bus_id = bu.bus_id
                JOIN seats s
                    ON b.seat_id = s.seat_id
                ORDER BY b.booking_id DESC
            """)

            records = cursor.fetchall()

            print("\n===== BOOKING HISTORY =====")

            if not records:
                print("No booking records found.")
                return

            for record in records:
                print("\nBooking ID:", record["booking_id"])
                print("Passenger:", record["passenger_name"])
                print("Bus:", record["bus_number"])
                print("Seat:", record["seat_number"])
                print("Date:", record["booking_date"])
                print("Amount: Rs.", record["total_amount"])
                print("Status:", record["booking_status"])

        except Error as error:
            print("Database Error:", error)

        finally:
            cursor.close()
