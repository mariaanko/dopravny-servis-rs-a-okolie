import json
import os
import time
from datetime import datetime, timedelta

import schedule

import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from post_photo import post_single_photo

# Define the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://embed.waze.com/iframe?zoom=11&lat=48.393650&lon=20.020523&ct=livemap',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cookie': 'ads-cookie-consent=allow; phpbb3_waze_u=1; phpbb3_waze_k=; ',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'trailers'
}


def scraper():
    print("scraper started!")
    try:
        url = ("https://embed.waze.com/live-map/api/georss?top=48.630850766928205&"
               "bottom=48.099847471402825&left=19.50052642822266&right=20.409370422363285&env=row"
               "&types=alerts,traffic")

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.content.decode()
            print('got response from source')

            json_data = json.loads(data)

            for alert in json_data['alerts']:
                try:
                    city = alert['city']
                    street = alert['street']
                    report_millis = alert['pubMillis']
                    fmt_report_date = datetime.fromtimestamp(report_millis / 1000).strftime("%d-%m-%Y %H:%M:%S")
                    alert_type = str(alert['type'])
                    location_x = str(alert['location']['x'])
                    location_y = str(alert['location']['y'])
                    time_now_seconds = datetime.now()
                    report_seconds = datetime.fromtimestamp(report_millis / 1000)
                    time_difference = time_now_seconds - report_seconds
                    defined_minutes = timedelta(minutes=30)
                    print("[" + fmt_report_date + "] : " + alert_type + "-> " + street + ", " + city + " \n")
                    if time_difference <= defined_minutes:
                        if alert_type == "POLICE" or alert_type == "ACCIDENT":
                            options = Options()
                            options.binary_location = '/usr/bin/google-chrome'
                            options.add_argument('--headless=new')
                            options.add_argument("--start-maximized")
                            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                                      options=options)
                            url = "https://maps.google.com/?q=" + location_y + "," + location_x + "&z=20"
                            driver.get(url)
                            driver.implicitly_wait(3)
                            driver.find_element(By.XPATH, "//button/span").click()
                            driver.implicitly_wait(3)
                            driver.get_screenshot_as_file(fmt_report_date + ".png")
                            print("screenshot saved! name: " + fmt_report_date + ".png \n")
                            message = (
                                        "[" + fmt_report_date + "] : " + alert_type + "-> " + street + ", " + city + " \n")
                            driver.close()
                            page_id = 122110656932277370
                            facebook_access_token = os.environ.get('FB_TOKEN')
                            try:
                                post_single_photo(page_id, facebook_access_token, message,
                                                  photo_url="./" + fmt_report_date + ".png")
                                print("posted successfully")
                            except requests.exceptions.RequestException as e:
                                # TODO: send email when fb request fails
                                print("Error:", response.status_code)
                                print(e)

                    else:
                        print("nothing to report")
                except KeyError:
                    # when something fails
                    continue
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    print("Process started!")
    schedule.every(30).minutes.do(scraper)
    print("Scheduled!")
    while True:
        schedule.run_pending()
        time.sleep(1)
