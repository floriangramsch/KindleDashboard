from PIL import Image, ImageDraw, ImageFont
# from create_dashboard import create_dashboard
from create_dashboard import Dashboard
import requests
import locale
import os
from datetime import datetime, timedelta
import time
time.tzset()

# optional sanity check
locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
os.environ["TZ"] = "Europe/Berlin"


def sleep_until_next_hour():
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0,
                                                   second=0, microsecond=0)
    seconds_until_next_hour = (next_hour - now).total_seconds()
    if seconds_until_next_hour > 0:
        print(f"Sleeping for {seconds_until_next_hour}s...")
        time.sleep(seconds_until_next_hour)
    else:
        # Sleep at least a short time to avoid busy loop
        print(f"Sleeping for {10}s...")
        time.sleep(10)


def should_run_now():
    now = datetime.now()
    start_hour = 8
    end_hour = 22

    return (start_hour <= now.hour < end_hour)


if (__name__ == "__main__"):
    nc_url = 'https://cloud.floxsite.de/remote.php/webdav/KindleDashboard/dashboard.png'
    username = os.environ.get('NC_USERNAME')
    password = os.environ.get('NC_PASSWORD')

    while True:
        if (should_run_now()):
            print(
                f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Creating dashboard...")
            # create_dashboard()
            dashboard = Dashboard()
            dashboard.create_dashboard()

            print(
                f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Uploading PNG...")
            with open('public/kindle_dashboard.png', 'rb') as f:
                r = requests.put(nc_url, data=f, auth=(username, password))
                print(
                    f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] Upload status:", r.status_code)
            print()

        sleep_until_next_hour()
