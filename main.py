import json
import time
import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
import uvicorn

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

def setup_driver():
    """
    Sets up a Chrome driver with options to run headless (no UI)
    and look like a real user to avoid blocking.
    """
    chrome_options = Options()
    
    # Run in headless mode (no visible UI)
    chrome_options.add_argument("--headless=new") 
    
    # Critical flags for Docker/Linux/Server environments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Set a real user agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_forex_factory_data():
    driver = None
    try:
        driver = setup_driver()
        url = "https://www.forexfactory.com/calendar"
        
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Give it a few seconds to load the JavaScript variables
        time.sleep(3) 
        
        # Extract the data directly from the window object
        data_dump = driver.execute_script("return window.calendarComponentStates;")
        
        if not data_dump:
            print("Error: window.calendarComponentStates was empty.")
            return None

        extracted_events = []

        # Iterate over values to find the one containing 'days'
        for key, value in data_dump.items():
            if 'days' in value:
                for day in value['days']:
                    for event in day.get('events', []):
                        
                        timestamp = event.get('dateline')
                        utc_string = "N/A"
                        
                        if timestamp:
                            # Convert Unix timestamp to UTC object
                            dt_object = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                            utc_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')

                        # Logic: If 'revision' exists, the website displays 'revision'.
                        # Otherwise, it displays the original 'previous'.
                        raw_previous = event.get('previous', '')
                        raw_revision = event.get('revision', '')
                        display_previous = raw_revision if raw_revision else raw_previous

                        extracted_events.append({
                            "title": event.get('name'),
                            "country": event.get('country'),
                            "currency": event.get('currency'),
                            "impact": event.get('impactTitle'),
                            "forecast": event.get('forecast', ''),
                            "previous": display_previous,
                            "actual": event.get('actual', ''),
                            "utc_timestamp": timestamp,
                            "utc_datetime": utc_string
                        })
                break

        return extracted_events

    except Exception as e:
        print(f"Selenium Error: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()

@app.get("/")
def home():
    return {"message": "Forex Selenium API is running. Go to /calendar"}

@app.get("/calendar")
def read_calendar():
    print("Received request for calendar...")
    data = get_forex_factory_data()
    
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to scrape data")
    
    return {
        "count": len(data),
        "timezone_info": "All times are in UTC",
        "events": data
    }

if __name__ == "__main__":
    # Get the port from the environment, default to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    # Host must be 0.0.0.0 for Docker/Render, NOT 127.0.0.1
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)