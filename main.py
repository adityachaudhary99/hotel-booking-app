import pandas as pd


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def available(self):
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False

    def book(self):
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv("hotels.csv", index=False)
        return "Hotel has been booked."


class SpaHotel(Hotel):
    pass


class Reservation:
    def __init__(self, customer_name, hotel_object):
        self.name = customer_name
        self.hotel = hotel_object

    def generate(self):
        return f"""
                Thank You for Your Reservation!
                Here are your booking data:
                Name: {self.name}.
                Hotel Name: {self.hotel.name}
                """


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, holder, expiration, cvv):
        card_data = {"number": self.number, "expiration": expiration,
                     "cvc": cvv, "holder": holder.upper()}

        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, user_password):
        password = df_cards_security.loc[df_cards_security['number'] == self.number, 'password'].squeeze()
        if password == user_password:
            return True
        else:
            return False


class SpaTicket:
    def __init__(self, spa_enquiry, name, hotel):
        self.spa_enquiry = spa_enquiry
        self.name = name
        self.hotel = hotel

    def generate(self):
        return f"""
                Thank You for Your Spa Reservation!
                Here are your booking data:
                Name: {self.name}.
                Hotel Name: {self.hotel.name}
                """


df = pd.read_csv("hotels.csv", dtype={"id": str})
print(df)

df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient='records')

df_cards_security = pd.read_csv("card_security.csv", dtype=str)

id = input("Enter the id of the hotel: ")

hotel = SpaHotel(id)

if hotel.available():
    card_number = input("Enter credit card number: ")
    card_holder_name = input("Enter credit card holder name: ")
    expiration_date = input("Enter expiration date: ")
    cvc = input("Enter cvc: ")
    credit_card = SecureCreditCard(number=card_number)

    if credit_card.validate(holder=card_holder_name, expiration=expiration_date, cvv=cvc):
        password = input("Enter credit card password: ")
        if credit_card.authenticate(password):
            hotel.book()
            name = card_holder_name.upper()
            reservation_ticket = Reservation(name, hotel)
            print(reservation_ticket.generate())

            spa_enquiry = input("Do you want to book a spa package?: ")

            spa = SpaTicket(spa_enquiry, card_holder_name, hotel)
            if spa_enquiry == 'yes':
                print(spa.generate())
            else:
                print("You opted not to book the spa package. Enjoy the vacation.")
        else:
            print("Credit Card authentication failed.")
    else:
        print("Credit card is not valid.")
else:
    print("Hotel is not available.")

