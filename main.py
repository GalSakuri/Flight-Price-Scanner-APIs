import requests
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

data_manager = DataManager()
flight_search = FlightSearch()
send_email = NotificationManager()

token = flight_search.api_token
sheet_data = data_manager.get_data()

for row in sheet_data:
    if not row["iataCode"]:
        row["iataCode"] = flight_search.get_iataCode(row["city"])
        data_manager.put_iataCode()

    temp = flight_search.get_price(
        row["iataCode"], row["adults"], row["children"])

    if not temp:
        print(f"No Flights offers found for {row["iataCode"]}")
        continue

    update_row = temp

    data_manager.update_price_info(
        row["id"], row["adults"], row["children"], update_row)

    if float(update_row["price"]["total"]) <= float(row["targetPrice"]):
        send_email.price_reach_send_email(update_row)
