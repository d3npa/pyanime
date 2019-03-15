import json, urllib.request, urllib.parse
from bs4 import BeautifulSoup
la = "0a9de5a4";

def episode(url, quality=720):
    # URLからラーバンのリンクを取得
    def gen_token(o, la):
        def sum(string):
            a = 0
            for i in range(len(string)):
                a += ord(string[i]) + i
            return a
        def secret(t, i):
            e = 0
            for n in range(max(len(t), len(i))):
                e *= ord(i[n]) if n < len(i) else 1
                e *= ord(t[n]) if n < len(t) else 1
            return hex(e)
        r = sum(la)
        for key in o:
            r += sum(secret(la + key, o[key]))
        return r - 49

    episode_id = url.split("/")[-1]
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    print("[*] [9anime] Getting details for episode '%s'" % episode_id)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    data = {
        "id" : episode_id,
        "server" : "33", # RapidVideo
        "ts" : soup.select_one("html")["data-ts"]
    }
    data.update({
        "_" : gen_token(data, la)
    })
    data = urllib.parse.urlencode(data)
    url = "https://www4.9anime.to/ajax/episode/info?" + data
    print("[*] [9anime] Getting links for episode '%s'" % episode_id)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    url = json.loads(res)["target"] + "&q=%dp" % quality
    print("[*] [RapidVideo] Getting '%s' at %dp" % (url.split("/")[-1].split("&")[0], quality))
    headers = {
        "Authority" : "www.rapidvideo.com",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer" : url,
        "Content-Type" : "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Range": "bytes=0-"
    }
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    try:
        res = {
            "link" : soup.select_one("#videojs > source:last-child")["src"]
        }
        return json.dumps(res)
    except:
        return 

def series(url):
    def magic(i):
        e = 0
        for n in range(len(i)):
            e += ord(i[n]) + n
        return e
    series_id = url.split(".")[-1]
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    print("[*] [9anime] Loading page for series '%s'" % series_id)
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(res, "html.parser")
    # AJAXリクエストを用意する
    data = urllib.parse.urlencode({
        "gresponse" : "03AHqfIOkU4OQabkZY16zwY-UEaw7thSLjjN43qmZXQ9fHt-AjzwBKVIddqgw6NO3jE1lU26ms7LP98jUDwSzB5_SOc_0n5lL6FCYR4vIlefwo5xwEIhD9cAqmiT8lsuVBAgMCfbBixm_TCTuLUbjlooIha_5pbvsWiLDIvs1JwQyFJQzXTsG2KLR3tVN_6vWdE7b7a_nxe6AcwIY9mDLu1t4N4t5hr7Dy84JwZ79zYa4Ec_GKJ96rxC5ub75ux8ktQeVcReQuBqUvhKnyeqSPqW2OdS_rYMXd4g",
        "ts" : soup.select_one("html")["data-ts"],
        "_" : magic(la) - 1
    })
    url = "https://www8.9anime.to/ajax/film/servers/%s?%s" % (series_id, data)
    print("[*] [9anime] Fetching episode list for series '%s'" % series_id)
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
