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
    df.set_index('timestamp', inplace=True)
    return df

def get_data_by_id(deviceId):
    df = pd.DataFrame(columns=['timestamp', 'co2', 'temperature', 'humidity']).set_index('timestamp')
    for week in tqdm(range(1, weeks)):
        data = get_week_data_by_id(deviceId, week)
        df = pd.concat([df, data])
        sleep(1)
    return df