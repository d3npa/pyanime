#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template, redirect, request, abort
from mimetypes import guess_type as guess_mime
import os, time, re, base64
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

extensions = {}
for extension in os.listdir("extensions"):
    path = "extensions/" + extension
    if os.path.isfile(path) and extension[-3:] == ".py":
        extension = extension[:-3]
        exec("import extensions.%s as ext" % extension)
        extensions.update({extension : ext})
        print("[*] 「%s」拡張をロードしました" % extension)
        del(ext)

@app.before_request
def log_request():
    remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
    line = "[{0}] - {1} \"{3} {2}\" - UA: {4}".format(
        time.strftime("%y/%m/%d %H:%M:%S"),
        remote_addr,
        str(request.url),
        request.method,
        request.headers["User-Agent"])
    print(line)

@app.route("/res/<path:path>")
def view_resource(path):
    path = "res/" + path
    if not os.path.exists(path):
        return make_response(render_template("404.jinja", filename=filename), status=404)
    with open(path, "rb") as f:
        res = make_response(f.read())
        res.headers["Content-Type"] = guess_mime(path) + "; charset=UTF-8"
        return res

@app.route("/robots.txt")
def robots_txt():
    res = make_response("User-agent: *\nDisallow: /", status=200)
    res.headers["Content-Type"] = "text/plain;"
    return res

@app.route("/")
def index():
    return make_response("生きてらの！")

@app.route("/<site>/search/<string:terms>")
def search(site, terms):
    if site in extensions:
        res = extensions[site].search(terms)
        if res:
            res = make_response(res)
            res.headers["Content-Type"] = "application/json; charset=UTF-8"
            return res
    abort(404)

@app.route("/<site>/series/<string:url>")
def series(site, url): # エピソード一覧を取得する
    if site in extensions:
        url = base64.b64decode(url).decode("utf-8")
        res = extensions[site].series(url)
        if res:
            res = make_response(res)
            res.headers["Content-Type"] = "application/json; charset=UTF-8"
            return res
    abort(404)

@app.route("/<site>/episode/<string:url>")
@app.route("/<site>/episode/<string:url>/<string:quality>")
def episode(site, url, quality="720"): # エピソード一覧を取得する
    if site in extensions and quality in ["360", "480", "720", "1080"]:
        url = base64.b64decode(url).decode("utf-8")
        res = extensions[site].episode(url, quality=int(quality))
        if res:
            res = make_response(res)
            res.headers["Content-Type"] = "application/json; charset=UTF-8"
            return res
    abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
