import json
from datetime import datetime, timedelta

import schedule

import requests

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
            print("---------------------------------------------------------------")
            print("---------------------------------------------------------------")
            data = response.content.decode()
            print(datetime.now())
            print("---------------------------------------------------------------")
            print("---------------------------------------------------------------")
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
                    defined_minutes = timedelta(minutes=15)
                    print("[" + fmt_report_date + "] : " + alert_type + "-> " + street + ", " + city + " \n")
                    if time_difference <= defined_minutes:
                        if alert_type == 'POLICE' or alert_type == 'ACCIDENT':
                            url = "https://maps.google.com/?q=" + location_y + "," + location_x + "&z=20"
                            try:
                                print(url)
                            except requests.exceptions.RequestException as e:
                                # TODO: send email when fb request fails
                                return None
                                print("Error:", response.status_code)
                                print(e)

                    else:
                        print('')
                    return json_data['alerts']
                except KeyError:
                    # when something fails
                    continue
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    print("Process started!")
    scraper()
    schedule.every(2).minutes.do(scraper)
    print("Scheduled!")
    while True:
        schedule.run_pending()
        # time.sleep(1)
