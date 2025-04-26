# Flight Price Checker & Alert

A Python script that:

- Reads a list of destination cities (and optional adults/children counts) from a Google Sheet  
- Looks up IATA codes and retrieves round-trip flight-offer data via the Amadeus API  
- Finds the cheapest offer and writes its details back to the sheet  
- Sends you an email alert when the price meets your target  

---

## Features

- **Automatic IATA lookup** for any city  
- **Configurable origin** airport (changeable in the Google Sheet)  
- **Currency selection** (default: GBP, easily changeable)  
- **Google Sheets integration** via Sheety (GET + PUT)  
- **Email alerts** when cheapest price ≤ your target  

---

## Files

- `main.py`  
  Orchestrates the workflow: fetch sheet data → ensure IATA codes → get cheapest flight → update sheet → send email  
- `flight_search.py`  
  `FlightSearch` class: handles Amadeus token, IATA lookups, and flight-offer requests  
- `data_manager.py`  
  `DataManager` class: GETs and PUTs rows in your Google Sheet via Sheety  
- `notification_manager.py`  
  `NotificationManager` class: formats and sends UTF-8 email alerts  

---

## Setup

1. Clone this repo  
   ```bash
   git clone https://github.com/your-user/flight-price­-checker.git
   cd flight-price-checker
   ```

2. Create & activate a virtual environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies  
   ```bash
   pip install requests pandas python-dotenv
   ```

4. Configure environment variables  
   Create a file named `.env` in the project root with these entries:  
   ```ini
   # Amadeus API credentials
   AMADEUS_CLIENT_ID=your_amadeus_api_key
   AMADEUS_CLIENT_SECRET=your_amadeus_api_secret

   # Sheety endpoints
   SHEETY_GET_URL=https://api.sheety.co/…/flightPrices/prices
   SHEETY_PUT_URL=https://api.sheety.co/…/flightPrices/prices

   # Email (used for alerts)
   MY_EMAIL=you@example.com
   EMAIL_PASSWORD=your_email_password
   ```

5. Set your default origin IATA  
   In `flight_search.py`, by default we call:  
   ```python
   self.default_airpot = self.get_iataCode("Tel Aviv")
   ```  
   Change `"Tel Aviv"` to your home-airport city (or directly to its IATA code).

6. Set your currency  
   In `flight_search.py` inside the `get_price` method, add:  
   ```python
   "currencyCode": "YOUR DESIRED CURRENCY",
   ```  
   Change `"GBP"` (the default) to your desired 3-letter currency code (e.g. `"ILS"`, `"USD"`, etc.).

---

## Usage

1. Populate your Google Sheet  
   - Columns: `id`, `city`, `iataCode` (can be blank), `adults`, `children`, `targetPrice`  
   - Fill `city` and `targetPrice`—the script will fill in IATA codes and pricing info.

2. Run the script  
   ```bash
   python main.py
   ```  
   - It will update each row with the cheapest offer details (minPrice, departureDate, arrival, etc.).  
   - If the price ≤ `targetPrice`, you’ll receive an email alert.

---

## Customization

- **Sheet columns**  
  If you rename or add columns, adjust `DataManager.get_data()` and `update_price_info()` to match.

- **Notification logic**  
  Tweak `NotificationManager.price_reach_send_email()` to include extra details or send to multiple addresses.

- **Automation**  
  To run automatically (e.g. daily), add a cron job or GitHub Action that calls `python main.py`.

---

## Dependencies

- Python 3.8+  
- `requests`  
- `pandas`  
- `python-dotenv`  

---

## License

This project is released under the MIT License.  
```
