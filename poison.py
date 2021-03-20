#!/usr/bin/python3

from bottle import redirect, response, route, run, template
import random as r
from string import ascii_letters

NAME_FILE = "names.csv"

LIST = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<title>Email List - page {{page}}</title>
<meta name=ROBOTS content="NOINDEX,NOFOLLOW">
<link rel=stylesheet href="/style">
<link rel=first href="/list/0">
%if page > 0:
<link rel=prev href="/list/{{prev}}">
%end
<link rel=next href="/list/{{next}}">
<h1>Email List (page {{page}})</h1>
<p>
%if page > 0:
<a href="/list/{{prev}}">Previous</a> | 
%end
<a href="/list/{{next}}">Next</a>
<hr>
<p>
"""

def emails(n):
    r.seed(n)
    return ["{}{}@{}.com".format(''.join([r.choice(ascii_letters) for l in range(3)]),
            r.randrange(10000), ''.join([r.choice(ascii_letters) for l in range(10)]))
            for e in range(20)]

@route("/robots.txt")
def robots():
    response.content_type = "text/plain; charset=UTF-8"
    return "User-agent: *\nDisallow: /"

@route("/style")
def style():
    response.content_type = "text/css; charset=UTF-8"
    return "body{background-color:#EEE;font-family:monospace}"

@route("/")
@route("/list")
@route("/list/")
def root():
  redirect("/list/0")

@route("/list/<pg:int>")
def maillist(pg=0):
    return template(LIST,page=pg,prev=pg-1,next=pg+1) + "<br>\n".join(
         ["<a href='mailto:{}'>{}</a>".format(e,e) for e in emails(pg)])

run(host='localhost', port=8081, debug=True)

