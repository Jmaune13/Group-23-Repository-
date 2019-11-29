import sqlite3

import click
import flask
import newsapi
from flask import Flask, Response
from flask import current_app, g
from flask.cli import with_appcontext
from webargs import fields
from webargs.flaskparser import use_args
from flask_json import FlaskJSON, as_json_p

app = Flask(__name__)
FlaskJSON(app)

@app.route('/')
def homepage():
    return flask.send_file('html/index.html')

@app.route('/<string:filename>')
def html(filename):
    return flask.send_file('html/' + filename)

@app.route('/img/<string:filename>')
def img(filename):
    return flask.send_file('img/' + filename)

@app.route('/css/<string:filename>')
def css(filename):
    return flask.send_file('css/' + filename)

@app.route('/js/<string:filename>')
def js(filename):
    return flask.send_file('js/' + filename)

def get_news_api():
    if 'news_api' not in g:
        with open('api_key.txt', 'r') as api_key:
            g.news_api = newsapi.NewsApiClient(api_key=api_key.read().strip())
    return g.news_api

@app.route('/api/get_news')
@use_args({
        "whitelist": fields.Str(required=False),
        "blacklist": fields.Str(required=False),
        "q": fields.Str(required=False),
        "sort": fields.Str(required=False),
        "category": fields.Str(required=False),
        "from-date": fields.Str(required=False),
        "to-date": fields.Str(required=False),
        "category": fields.Str(required=False),
        "lang": fields.Str(required=False),
    })
@as_json_p
def get_news(args):
    use_whitelist = "whitelist" in args
    whitelist = args["whitelist"].split(',') if use_whitelist else []
    blacklist = args["blacklist"].split(',') if "blacklist" in args else []
    sort = args["sort"] if "sort" in args else "relevance"
    q = args["q"] if "q" in args else ""
    lang = args["lang"] if "lang" in args else "en"

    newsapi = get_news_api()

    return newsapi.get_top_headlines(
            q=q,
            sources='bbc-news,the-verge,associated-press',
            language=lang)

category_options = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

if __name__ == '__main__':
    app.run()
