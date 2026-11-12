
class Passenger:
    def __init__(
        self,
        passenger_id,
        passenger_name,
        email,
        phone
    ):
        self.passenger_id = passenger_id
        self.passenger_name = passenger_name
        self.email = email
        self.phone = phone

    def display_passenger(self):
        print("\n===== PASSENGER DETAILS =====")
        print("Passenger ID:", self.passenger_id)
        print("Passenger Name:", self.passenger_name)
        print("Email:", self.email)
        print("Phone:", self.phone)
