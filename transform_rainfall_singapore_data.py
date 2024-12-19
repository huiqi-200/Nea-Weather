import polars as pl
import json
import os

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    records = []
    for item in data["items"]:
        timestamp = item["timestamp"]
        for reading in item["readings"]:
            records.append({
                "timestamp": timestamp,
                "station_id": reading["station_id"],
                "value": reading["value"]
            })
    
    return records

def create_dataframe_from_folder(folder_path):
    all_records = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            all_records.extend(process_json_file(file_path))
    
    schema = {
        "timestamp": pl.String,
        "station_id": pl.Utf8,
        "value": pl.Int64
    }
    
    df = pl.DataFrame(all_records, schema=schema)
    # Convert the 'timestamp' column to datetime type, and in SGT
    df = df.with_columns( 
        pl.col("timestamp").str.strptime(pl.Datetime, format="%Y-%m-%dT%H:%M:%S%z").dt.convert_time_zone("Asia/Singapore")
    )
    return df

def get_max_value_per_hr(df):
    # Group by 'station_id' and hourly 'timestamp', then get the max 'value'
    result = df.with_columns(
        pl.col("timestamp").dt.hour().alias("hour"),
        pl.col("timestamp").dt.date().alias("date")
    ).group_by(["station_id", "Date", "hour"]).agg(
        pl.col("value").max().alias("max_value")
    )
    return result

# Example usage
folder_path = "sample_raw"
df = create_dataframe_from_folder(folder_path)
print(df)
agg_df = get_max_value_per_hr(df)
agg_df.write_csv(file="test.csv", date_format="%Y-%m-%d")