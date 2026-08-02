import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.leagueoflegends.com/en-us/news/tags/patch-notes/"

html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

article = soup.find("a", href=True)

while article and "/news/" not in article["href"]:
    article = article.find_next("a", href=True)

if article is None:
    raise Exception("Couldn't find patch notes.")

title = article.get_text(strip=True)
link = article["href"]

if link.startswith("/"):
    link = "https://www.leagueoflegends.com" + link

state = "last_patch.txt"

last = ""
if os.path.exists(state):
    last = open(state).read().strip()

if link != last:
    payload = {
        "embeds": [{
            "title": title,
            "url": link,
            "description": "🎮 A new League of Legends patch has been released!",
            "color": 3447003
        }]
    }

    r = requests.post(WEBHOOK, json=payload)
    r.raise_for_status()

    with open(state, "w") as f:
        f.write(link)

    print("Posted new patch.")
else:
    print("No new patch.")
