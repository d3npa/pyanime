import json, urllib.request, urllib.parse
from bs4 import BeautifulSoup

def search(terms):
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    url = "https://www4.9anime.to/search?keyword=" + urllib.parse.quote(terms)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    results = set(soup.select("div.item > div.inner > a.poster > img"))
    res = []
    for entry in results:
        res.append({
            "title" : entry["alt"],
            "poster" : entry["src"],
            "link" : entry.parent["href"]
        })
    return json.dumps(res)
