import datetime as dt
import random
import smtplib
import pandas as pd

my_email = "YOUR_EMAIL"
to_addrs = "TO_ADDRES" 
password = "YOUR_PASSWORD"


class NotificationManager:

    def price_reach_send_email(self, offer):

        today = dt.datetime.now()

        departure = offer['itineraries'][0]['segments'][0]['departure']
        arrive = offer['itineraries'][0]['segments'][0]['arrival']
        price = offer['price']['total']
        carrier = offer['itineraries'][0]['segments'][0]['carrierCode']
        number = offer['itineraries'][0]['segments'][0]['number']

        subject = "Price Alert: Your flight deal has been found!"
        body = (
            f"Cheapest flight found on {today.strftime('%Y-%m-%d %H:%M')}:\n\n"
            f"Price: {price} GBP\n"
            f"Origin: {departure['iataCode']} at {departure['at'].replace('T', ', ')}\n"
            f"Destination: {arrive['iataCode']} at {arrive['at'].replace('T', ', ')}\n"
            f"Carrier: {carrier} Flight {number}\n"
        )
        msg = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_addrs,
                msg=msg
            )
