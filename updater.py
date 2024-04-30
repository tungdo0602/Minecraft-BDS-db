import requests
from bs4 import BeautifulSoup as BS
import json

data = {}

try:
    with open("versions.json", "r") as f:
        data = json.loads(f.read())
except:
    pass
res = requests.get("https://www.minecraft.net/en-us/download/server/bedrock", headers={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
})
if res.status_code == 200:
    print("Scraped Versions!")
    html = BS(res.text, "html.parser")
    elms = html.select(".downloadlink")
    for i in elms:
        if all(a in i.attrs for a in ["data-platform", "href"]):
            plat = i.attrs["data-platform"]
            link = i.attrs["href"]
            mcver = link[link.rindex("-")+1:].replace(".zip", "")
            if not mcver in data.keys(): data[mcver] = {"preview": "Preview" in plat}
            if any(a in plat for a in ["Windows", "Linux"]): data[mcver]["Windows" if "Windows" in plat else "Linux"] = link
    with open("versions.json", "w") as f:
        f.write(json.dumps(data))
    print("Updated!")
else:
    raise requests.ConnectionError("Failed! Status Code: {}".format(res.status_code))
