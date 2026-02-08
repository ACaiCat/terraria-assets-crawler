import io

from bs4 import BeautifulSoup, Tag
import httpx
from PIL import Image
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'User-Agent': ua.random
}

with open("data.html", mode='rt') as f:
    html: str = f.read()

soup = BeautifulSoup(html, 'html.parser')

table: Tag = soup.find('table').find('tbody')
rows = table.find_all('tr')

for row in rows:
    columns = row.find_all('td')
    _id = int(columns[0].text)

    if _id < 0:
        continue

    try:
        img_link = columns[2].find('img').get('src')
    except Exception as ex:
        print(columns[2])
        print(ex)
        img_link = ""
    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        if not img_link:
            break
        try:
            with httpx.Client(base_url="https://terraria.wiki.gg/", headers=headers) as client:
                response: httpx.Response = client.get(img_link)
                response.raise_for_status()

                image = Image.open(io.BytesIO(response.content))
                image.save(f"imgs/NPC_{_id}.png", 'PNG', optimize=True, save_all=True)
                print(img_link)
                break
        except Exception as ex:
            attempts += 1
            if attempts == max_attempts:
                raise ex
            print(f"重试 {attempts}/{max_attempts}: {img_link}")
