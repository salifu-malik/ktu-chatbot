import requests
import time
import threading

# Global variable to store cached data
ktu_data_cache = []

def fetch_ktu_data():
    """
    Fetches data from a temporary test API (simulating KTU API).
    Replace this URL with the real API later.
    """
    global ktu_data_cache
    try:
        # Example mock API with sample data
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # We'll only keep first few records for simplicity
        ktu_data_cache = [
            {
                "question": item["title"],
                "answer": item["body"]
            }
            for item in data[:5]
        ]

        print("✅ KTU data refreshed successfully.")
    except Exception as e:
        print("⚠️ Error fetching KTU API data:", e)


def schedule_weekly_refresh():
    """
    Automatically refreshes data every week (7 days).
    Runs in a background thread.
    """
    def refresh_loop():
        while True:
            fetch_ktu_data()
            # Sleep for 7 days (in seconds)
            time.sleep(7 * 24 * 60 * 60)

    # Start background thread
    thread = threading.Thread(target=refresh_loop, daemon=True)
    thread.start()
