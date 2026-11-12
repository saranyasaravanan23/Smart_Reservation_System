
from db_connection import get_connection
from bus import Bus
from booking import Booking
from waiting_list import WaitingList


def main():

    connection = get_connection()

    if connection is None:
        print("Unable to connect to MySQL database.")
        return

    try:
        while True:

            print("\n===== BUS RESERVATION SYSTEM =====")
            print("\n1. Add Bus")
            print("2. Search Buses")
            print("3. View Available Seats")
            print("4. Book Ticket")
            print("5. Cancel Ticket")
            print("6. View Booking History")
            print("7. View Waiting List")
            print("8. Exit")

            choice = input("\nEnter Your Choice: ").strip()

            if choice == "1":
                Bus.add_bus(connection)

            elif choice == "2":
                Bus.search_buses(connection)

            elif choice == "3":
                try:
                    bus_id = int(input("Enter Bus ID: "))
                    Booking.view_available_seats(connection, bus_id)
                except ValueError:
                    print("Please enter a valid Bus ID.")

            elif choice == "4":
                Booking.book_ticket(connection)

            elif choice == "5":
                Booking.cancel_ticket(connection)

            elif choice == "6":
                Booking.view_booking_history(connection)

            elif choice == "7":
                WaitingList.view_waiting_list(connection)

            elif choice == "8":
                print("\nThank you for using Bus Reservation System!")
                break

            else:
                print("Invalid choice. Please select 1 to 8.")

    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
