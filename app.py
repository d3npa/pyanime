#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template, redirect, request, abort
from mimetypes import guess_type as guess_mime
import os, time, re
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

@app.after_request
def log_request(res):
    remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
    line = "{1} - [{0}] \"{4} {2}\" {3} - UA: {5}".format(
        time.strftime("%y/%m/%d %H:%M:%S"),
        remote_addr,
        str(request.url),
        res.status_code,
        request.method,
        request.headers["User-Agent"])
    print(line)
    return res

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
        res = make_response(res)
        res.headers["Content-Type"] = "application/json; charset=UTF-8"
        return res
    abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
