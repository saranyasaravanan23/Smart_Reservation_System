
# Smart Bus Ticket Booking & Reservation System

## Project Information
**Task Name:** Smart Bus Ticket Booking & Reservation System

**Technology Used:**
- Python
- Object-Oriented Programming (OOP)
- MySQL
- SQL Transactions
- Exception Handling

## Project Description
This is a console-based bus ticket booking application developed using Python and MySQL.

Users can add buses, search buses by source and destination, check seat availability, book tickets, cancel tickets, view booking history and manage waiting lists.

## Project Features
1. Add Bus
2. Search Buses
3. View Available Seats
4. Book Ticket
5. Cancel Ticket
6. View Booking History
7. View Waiting List
8. Exit

## Database Tables
The project uses the following MySQL tables:

- routes
- buses
- passengers
- seats
- bookings
- waiting_list

## Project Structure
```text
Smart_Bus_Reservation_System/
│
├── main.py
├── db_connection.py
├── bus.py
├── passenger.py
├── booking.py
├── waiting_list.py
├── requirements.txt
├── README.md
│
├── database/
│   └── bus_reservation.sql
│
└── screenshots/
```

## Installation

Install the required package:

```bash
python -m pip install -r requirements.txt
```

## Database Configuration

1. Open MySQL Workbench.
2. Create the database `user_management_db` if it does not already exist.
3. Execute the SQL file inside the database folder.
4. Update the MySQL username and password in `db_connection.py`.

## Run the Application

Open the terminal inside the project folder and execute:

```bash
python main.py
```

## Booking Process

1. Search for buses using source and destination.
2. Check available seats.
3. Enter passenger details.
4. Select the bus and seat number.
5. Confirm the ticket booking.
6. The system generates a unique booking ID.
7. The ticket amount is calculated using the route ticket price.

## Cancellation and Waiting List

- Users can cancel confirmed tickets using the booking ID.
- Cancelled tickets are stored in booking history.
- When a bus has no available seats, passengers can be added to the waiting list.
- When a confirmed ticket is cancelled, the oldest waiting passenger is automatically allocated the released seat.

## SQL Transactions

SQL transactions are used during bus creation, ticket booking and cancellation.

- COMMIT saves successful database changes.
- ROLLBACK reverses changes when an error occurs.
- Row locking helps prevent simultaneous booking of the same seat.

## Exception Handling

The application handles:
- Invalid user input
- Invalid bus ID
- Invalid seat number
- Already booked seats
- Duplicate passenger details
- Database errors

## Testing

The following operations should be tested:

1. Add a new bus.
2. Search for a bus.
3. View available seats.
4. Book a ticket successfully.
5. Try booking an already booked seat.
6. Cancel a confirmed ticket.
7. Check booking history.
8. Add a passenger to the waiting list when the bus is full.
9. Check automatic waiting-list allocation after cancellation.

## Conclusion

The Smart Bus Ticket Booking & Reservation System provides a simple console-based solution for bus reservation using Python, OOP concepts and MySQL database operations.
```

Save using `Ctrl + S`.

**Next:** Run `python main.py` and verify the menu works. Don't create any additional files now.