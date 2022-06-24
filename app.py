from insights import Insights
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)

nxt, client = None, None


@app.get('/')
def get_hashtag_posts():
    global client
    global nxt
    client = Insights(
        os.getenv('user_id'),
        os.getenv('access_token'),
        request.args.get('hashtag')
    )
    data = client.fetch_hashtag_posts()
    nxt = data['paging']['cursors']['after']

    data = data['data']

    # calculate like to comment ratio on each item
    data = map(
        update_obj,
        data
    )

    data = list(data)

    if 'sort' in request.args:
        param = request.args.get('sort')
        resp = sort_by_param(param, data)

        return jsonify(
            resp
        )
    return jsonify(data)


@app.get('/next')
def fetch_next():
    global client
    global nxt

    data = client.fetch_hashtag_posts(after=nxt)

    print(nxt, end="\n")

    nxt = data['paging']['cursors']['after']

    # calculate like to comment ratio on each item
    data = data['data']
    
    mods = map(
        update_obj,
        data
    )

    return jsonify(
        list(mods)
    )


app.run(debug=True)
