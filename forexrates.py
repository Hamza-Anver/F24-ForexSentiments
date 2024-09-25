import requests
import pandas as pd

url = "https://www.cbsl.gov.lk/cbsl_custom/exratestt/exrates_resultstt.php"
output_dir = "data/forex_rates.csv"

def get_forex_rates():
    

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    data = {
        "lookupPage": "lookup_daily_exchange_rates.php",
        "startRange": "2006-11-11",
        "rangeType": "dates",
        "txtStart": "2020-09-24",
        "txtEnd": "2024-09-24",
        "chk_cur[]": ["USD~United States Dollar"],
        "submit_button": "Submit"
    }

    response = requests.post(url, headers=headers, data=data)

    df = pd.read_html(response.text)

    df[0].to_csv(output_dir, index=False)

if __name__ == "__main__":
    get_forex_rates()