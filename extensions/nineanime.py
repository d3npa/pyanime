import json, urllib.request, urllib.parse
from bs4 import BeautifulSoup

def series(url):
    def magic(i):
        e = 0
        for n in range(len(i)):
            e += ord(i[n]) + n
        return e
    la = "0a9de5a4";
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    print("[*] Getting %s" % url)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    # AJAXリクエストを用意する
    data = urllib.parse.urlencode({
        "gresponse" : "03AHqfIOkU4OQabkZY16zwY-UEaw7thSLjjN43qmZXQ9fHt-AjzwBKVIddqgw6NO3jE1lU26ms7LP98jUDwSzB5_SOc_0n5lL6FCYR4vIlefwo5xwEIhD9cAqmiT8lsuVBAgMCfbBixm_TCTuLUbjlooIha_5pbvsWiLDIvs1JwQyFJQzXTsG2KLR3tVN_6vWdE7b7a_nxe6AcwIY9mDLu1t4N4t5hr7Dy84JwZ79zYa4Ec_GKJ96rxC5ub75ux8ktQeVcReQuBqUvhKnyeqSPqW2OdS_rYMXd4g",
        "ts" : soup.select_one("html")["data-ts"],
        "_" : magic(la) - 1
    })
    series_id = url.split(".")[-1]
    url = "https://www8.9anime.to/ajax/film/servers/%s?%s" % (series_id, data)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(json.loads(res)["html"], "html.parser")
    episodes = set(soup.select("div.server[data-name='33'] a"))
    res = []
    for episode in episodes:
        res.append({
            "number" : episode.contents[0],
            "link" : "https://www4.9anime.to" + episode["href"]
        })
    res = sorted(res, key=lambda x: float(x["number"]))
    return json.dumps(res)

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
