import requests
import json
from datetime import datetime, timedelta

def generate_date_list(start_date, end_date):
    date_list = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return date_list

# Example usage
start_date = "2023-01-01"
end_date = "2024-11-30"
dates = generate_date_list(start_date, end_date)


def get_json(date):
    url = f"https://api.data.gov.sg/v1/environment/rainfall/?date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

    
    with open(f"raw\\nea_weather_{date}.json", "w", encoding='utf8') as json_file: 
        json.dump(data, json_file, ensure_ascii=False)

for date in dates:
    get_json(date)