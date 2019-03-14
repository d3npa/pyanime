#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template, redirect, request
from mimetypes import guess_type as guess_mime
import os, time, re
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.after_request
def log_request(res):
    remote_addr = request.headers["X-Forwarded-For"] if "X-Forwarded-For" in request.headers else request.remote_addr
    line = "{1} - [{0}] \"{4} {2}\" {3} - UA: {5}".format(
        time.strftime("%y/%m/%d %H:%M:%S"),
        remote_addr,
        str(request.url), #  .encode("utf-8"),
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
