import requests, json
from headers import Headers
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup

start_date = datetime(2022, 9, 1)
weeks = datetime.now().isocalendar()[1] - start_date.isocalendar()[1]

def get_week_data_by_id(deviceId, week):
    url = "https://co2.mesh.lv/api/device/chart/"
    payload = {"deviceId":deviceId,"week":week,"captchaToken":"-1"}
    r = requests.post(url, json=payload)
    data = json.loads(r.text)['data']
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def get_data_by_id(deviceId, start_week=1, end_week=weeks):
    df = pd.DataFrame(columns=['timestamp', 'co2', 'temperature', 'humidity'])
    for week in tqdm(range(start_week, end_week)):
        data = get_week_data_by_id(deviceId, week)
        df = pd.concat([df, data])
        sleep(1)
    return df

def scrape_building(building_id, room_ids, start_week=1, end_week=weeks):
    df = pd.DataFrame(columns=['timestamp', 'room_id', 'co2', 'temperature', 'humidity'])
    for room_id in (t := tqdm(room_ids)):
        data = get_data_by_id(room_id, start_week=start_week, end_week=end_week)
        data['room_id'] = room_id
        df = pd.concat([df, data])
        t.set_description("Rooms")
    return df

if __name__ == "__main__":
    building_id = 1003
    rooms_df = pd.read_csv('data/rooms.csv')
    room_ids = rooms_df[rooms_df['building_id'] == building_id]['id'].values.tolist()
    df = scrape_building(building_id, room_ids)
    df.to_csv(f'data/{building_id}.csv', index=False)