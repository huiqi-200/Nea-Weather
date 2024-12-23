import requests
import json
from datetime import datetime, timedelta

def generate_date_list(start_date, end_date):
    """
    Generate a list of dates between the given start and end dates.

    Args:
        start_date (str): The start date in the format "yyyy-mm-dd".
        end_date (str): The end date in the format "yyyy-mm-dd".

    Returns:
        list: A list of dates as strings in the format "yyyy-mm-dd".

    """
    date_list = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    while current_date <= end_date:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return date_list

def get_json(date, folder='raw'):
    """
    For a given date, return the raw json rainfall data extracted from data.gov api
    A Json file will be saved under given folder 

    Args: 
        date (str): A given date in the format 'yyyy-mm-dd'

    Returns:
        None
    
    """
    url = f"https://api.data.gov.sg/v1/environment/rainfall/?date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with open(f"{folder}\\nea_weather_{date}.json", "w", encoding='utf8') as json_file: 
            json.dump(data, json_file, ensure_ascii=False)

    
# Example usage
start_date = "2023-01-01" # date to start extracting from
end_date = "2024-11-30" # date to start extracting till
folder_to_save_to = "raw" # folder to save json files to
dates = generate_date_list(start_date, end_date)

for date in dates:
    get_json(date, folder= folder_to_save_to)