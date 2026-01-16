# Forex-Calender-API
Forex Factory Calendar Unofficial API Using FastAPI

```test_client.py```
```
import requests
import json

# Your Render URL
url = "https://forex-calender-api.onrender.com/calendar"

print(f"Fetching data from {url}...")
print("NOTE: On Render Free Tier, this can take 60+ seconds if the server is waking up.")

try:
    # --- FIX: Increase timeout from 30 to 120 seconds ---
    # This gives the free server enough time to wake up and launch Chrome.
    response = requests.get(url, timeout=120) 
    
    if response.status_code == 200:
        data = response.json()
        
        filename = "live_calendar_data.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"\n[SUCCESS] Data saved to '{filename}'")
        print(f"Total Events: {data['count']}")
        print(f"Timezone: {data['timezone_info']}")
        
        print("\n--- Preview ---")
        for event in data['events'][:3]:
            print(f"[{event['utc_datetime']} UTC] {event['country']} - {event['title']}")

    else:
        print(f"[ERROR] Status Code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"[EXCEPTION] {e}")
```
<br>
<br>

```Response```
```
Fetching data from https://forex-calender-api.onrender.com/calendar...

[SUCCESS] Data saved to 'live_calendar_data.json'
Total Events: 101
Timezone: All times are in UTC

--- Preview ---
[2026-01-12 00:00:00 UTC] JN - Bank Holiday
[2026-01-12 00:30:00 UTC] AU - ANZ Job Advertisements m/m
[2026-01-12 00:30:00 UTC] AU - Household Spending m/m
```
