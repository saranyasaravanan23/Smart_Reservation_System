CREATE DATABASE IF NOT EXISTS user_management_db;

USE user_management_db;
USE user_management_db;

SHOW TABLES;
USE user_management_db;
SHOW TABLES;


USE user_management_db;

-- 1. Routes Table
CREATE TABLE IF NOT EXISTS routes (
    route_id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL,
    CHECK (ticket_price > 0),
    UNIQUE (source, destination, departure_time)
);

-- 2. Buses Table
CREATE TABLE IF NOT EXISTS buses (
    bus_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_number VARCHAR(30) NOT NULL UNIQUE,
    route_id INT NOT NULL,
    total_seats INT NOT NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id),
    CHECK (total_seats > 0)
);

-- 3. Passengers Table
CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL UNIQUE
);

-- 4. Seats Table
CREATE TABLE IF NOT EXISTS seats (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    bus_id INT NOT NULL,
    seat_number INT NOT NULL,
    seat_status ENUM('AVAILABLE', 'BOOKED') DEFAULT 'AVAILABLE',
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id),
    UNIQUE (bus_id, seat_number)
);

-- 5. Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT NOT NULL,
    bus_id INT NOT NULL,
    seat_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    booking_status ENUM('CONFIRMED', 'CANCELLED')
        DEFAULT 'CONFIRMED',
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id),
    FOREIGN KEY (seat_id) REFERENCES seats(seat_id),
    CHECK (total_amount > 0)
);

-- 6. Waiting List Table
CREATE TABLE IF NOT EXISTS waiting_list (
    waiting_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT NOT NULL,
    bus_id INT NOT NULL,
    booking_status ENUM('WAITING', 'ALLOCATED', 'CANCELLED')
        DEFAULT 'WAITING',
    waiting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id)
);
