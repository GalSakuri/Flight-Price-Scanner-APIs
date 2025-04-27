import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_OFFER_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:

    def __init__(self):
        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_API_SECRET"]
        self.api_token = self.get_token()
        self.default_airpot = self.get_iataCode("Tel Aviv")

    def get_token(self):

        header = {
            "Content-Type": "application/x-www-form-urlencoded"}

        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret, }

        response = requests.post(
            url=TOKEN_ENDPOINT, data=params, headers=header)

        token_data = response.json()
        return token_data["access_token"]

    def get_iataCode(self, city_name):

        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }

        params = {
            "keyword": city_name,
            "max": "1",
            "include": "AIRPORTS",
        }

        response = requests.get(
            url=IATA_ENDPOINT, params=params, headers=headers)
        city_iataCode = response.json()["data"][0]["iataCode"]

        return city_iataCode

    def get_city_name(self, iata_code):

        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }

        params = {
            "keyword": iata_code,
            "max": "1",
            "include": "AIRPORTS",
        }

        response = requests.get(
            url=IATA_ENDPOINT, params=params, headers=headers)
        city_name = response.json()["data"][0]["name"]
        return city_name

    def get_price(self, iata_code, adults, children):

        tomorrow = datetime.now() + timedelta(days=1)
        six_month = datetime.now() + timedelta(days=30*6)

        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }

        params = {
            "originLocationCode": self.default_airpot,
            "destinationLocationCode": iata_code,
            "departureDate": tomorrow.strftime("%Y-%m-%d"),
            "returnDate": six_month.strftime("%Y-%m-%d"),
            "adults": adults,
            "children": children,
            "currencyCode": "ILS",
            "max": "4",
        }

        response = requests.get(url=FLIGHT_OFFER_ENDPOINT,
                                params=params, headers=headers)

        if response.status_code != 200:
            print(
                f"A Problem accured in the flight search, code status: {response.status_code}")
            return None

        temp_json = response.json()
        offers = temp_json.get("data", [])

        if not offers:
            return {}

        min_price = float(offers[0]["price"]["total"])
        min_offer = offers[0]

        for offer in offers[0:]:
            price = float(offer["price"]["total"])
            if price < min_price:
                min_price = price
                min_offer = offer

        return min_offer
