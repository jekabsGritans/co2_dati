from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from tqdm import tqdm

#Get building names, addresses and ids
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

buildings_df = pd.DataFrame(columns=['id', 'name', 'address']).set_index('id')
url = "https://co2.mesh.lv/home/dashboard"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')[1:]

for row in rows:
    a_elem = row.find('a')
    location = a_elem.text.split(',')
    building_name = location[0].rstrip()
    building_address = ",".join(location[1:]).rstrip()
    building_id = a_elem['href'].split('/')[-1]
    buildings_df.loc[building_id] = [building_name, building_address]

buildings_df.to_csv('data/buildings.csv')

#Get rooms and device ids
driver = webdriver.Chrome("/usr/local/bin/chromedriver")

rooms_df = pd.DataFrame(columns=['id', 'name', 'building_id']).set_index('id')
for building_id in tqdm(buildings_df.index):
    url = f"https://co2.mesh.lv/home/building-devices/{building_id}"
    driver.get(url)
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    for row in rows:
        room_elem = row.find_all('td')[0]
        room_name = room_elem.text
        room_id = room_elem.find('a')['href'].split('/')[-1]
        rooms_df.loc[room_id] = [room_name, building_id]

rooms_df.to_csv('data/rooms.csv')
print(f"Found {len(rooms_df)} rooms and {len(buildings_df)} buildings")