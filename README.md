# Forex-Calendar-API

An unofficial, fast, reliable, and secure Forex Factory Calendar API built with **FastAPI** and **Selenium**. 

## 🚀 Features
- **Headless Selenium Scraping**: Bypasses bot-protections by mimicking real browsers.
- **Background Caching**: Scrapes data in the background (every 15 minutes) so that API requests return instantly without any timeout issues. Ideal for free-tier deployments (e.g., Render).
- **API Key Security**: Secured with an `X-API-Key` header to prevent unauthorized access. 

---

## 🛠 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Forex-Calender-API.git
cd Forex-Calender-API
```

### 2. Install dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Copy the `.env.sample` file to `.env`:
```bash
cp .env.sample .env
```
Open the `.env` file and define your secret API key:
```env
FOREX_API_KEY="your_secret_api_key_here"
```

### 4. Run the API Locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
*(The API will automatically start the background scraper upon launch. The server will be available at `http://localhost:8000`)*

---

## 📖 How to Use the API

### Endpoints
- `GET /` - Health check.
- `GET /calendar` - Returns the latest cached Forex Calendar events. **Requires authentication.**

### Authentication
All requests to `/calendar` must include your API Key in the `X-API-Key` HTTP header.

### Example Usage (Python)

```python
import requests
import json

# Replace with your deployed Render URL if running in production
url = "http://localhost:8000/calendar" 
api_key = "your_secret_api_key_here"

headers = {
    "X-API-Key": api_key
}

print(f"Fetching data from {url}...")
response = requests.get(url, headers=headers, timeout=30) 

if response.status_code == 200:
    data = response.json()
    print(f"[SUCCESS] Total Events: {data['count']}")
    print(f"Last Updated: {data.get('last_updated', 'N/A')}")
    print(f"Timezone: {data['timezone_info']}")
    
    print("\n--- Preview ---")
    for event in data['events'][:3]:
        print(f"[{event['utc_datetime']} UTC] {event['country']} - {event['title']}")
else:
    print(f"[ERROR] Status Code: {response.status_code}")
    print("Response:", response.text)
```

### Example Response Format
```json
{
    "count": 101,
    "timezone_info": "All times are in UTC",
    "last_updated": "2026-06-01 19:04:30",
    "events": [
        {
            "title": "Bank Holiday",
            "country": "JN",
            "currency": "JPY",
            "impact": "Non-Economic",
            "forecast": "",
            "previous": "",
            "actual": "",
            "utc_timestamp": 1705017600,
            "utc_datetime": "2026-01-12 00:00:00"
        }
    ]
}
```
