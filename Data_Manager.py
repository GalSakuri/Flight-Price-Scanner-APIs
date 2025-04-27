import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHEETY_get_ENDPOINT = os.environ["SHEETY_GET_ENDPOINT"]
SHEETY_put_ENDPOINT = os.environ["SHEETY_PUT_ENDPOINT"]


class DataManager:

    def get_data(self):
        response = requests.get(url=SHEETY_get_ENDPOINT)
        data = response.json()
        self.dataV1 = data["prices"]
        return self.dataV1

    def put_iataCode(self):
        for city in self.dataV1:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]}
            }

            response = requests.put(
                url=f"{SHEETY_put_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

    def update_price_info(self, row_id, row_adults, row_children, offer):
        new_data = {
            "price": {
                "adults": row_adults,
                "children": row_children,
                "minPrice": f"{offer["price"]["total"]} ₪",
                "flightCode": f"{offer["itineraries"][0]["segments"][0]["carrierCode"]} - {offer["itineraries"][0]["segments"][0]["number"]}",
                "originAirport": offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "departureDate": offer["itineraries"][0]["segments"][0]["departure"]["at"].replace('T', ' '),
                "destination": offer["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
                "arrival": offer["itineraries"][0]["segments"][0]["arrival"]["at"].replace('T', ' '),
            }
        }

        response = requests.put(
            url=f"{SHEETY_put_ENDPOINT}/{row_id}", json=new_data)

        print(f"updated row {row_id}: ", response.status_code, response.text)
