import pandas as pd
import requests
import time

API_KEY = 'YOUR_API_KEY'  # ←取得したAPIキーをここに記入

def get_latlon(address, api_key):
    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key, 'language': 'ja'}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return pd.Series([location['lat'], location['lng']])
    except Exception as e:
        print(f"Error: {e}")
    return pd.Series([None, None])

df = pd.read_csv('members-utf8.csv', header=None, names=['番号', '氏名', '郵便番号', '住所'])

results = []
for idx, row in df.iterrows():
    results.append(get_latlon(row['住所'], API_KEY))
    time.sleep(0.2)  # 連続アクセス対策

df[['緯度', '経度']] = results
df.to_csv('members_with_latlon.csv', index=False)