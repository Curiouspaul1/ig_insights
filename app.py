from insights import Insights
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, make_response, abort
from utils import *

app = Flask(__name__)

nxt, client = None, None
valid_sort_params = ['like_count', 'comments_count', 'like_comment_ratio']

@app.get('/')
def get_hashtag_posts():
    global client
    global nxt
    if 'hashtag' not in request.args or 'endpoint' not in request.args:
        resp = make_response(
            {
                'status': 'error',
                'msg': 'missing parameter "hashtag" or "endpoint" ',
                'data': []
            }, 400
        )
        abort(400)
    client = Insights(
        os.getenv('user_id'),
        os.getenv('access_token'),
        request.args.get('hashtag'),
        request.args.get('endpoint')
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
        if param not in valid_sort_params:
            return {
                'status': 'error',
                'msg': 'invalid sort param',
                'data': []
            }, 400
        if 'sort_order' in request.args:
            order = request.args.get('sort_order')
            resp = sort_by_param(param, data, desc=int(order))
        else:
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
    
    data = map(
        update_obj,
        data
    )

    data = list(data)

    if 'sort' in request.args:
        param = request.args.get('sort')
        if param not in valid_sort_params:
            return {
                'status': 'error',
                'msg': 'invalid sort param',
                'data': []
            }, 400
        
        if 'sort_order' in request.args:
            order = request.args.get('sort_order')
            resp = sort_by_param(param, data, desc=int(order))
        else:
            resp = sort_by_param(param, data)

        return jsonify(
            resp
        )

    return jsonify(data)

app.run(debug=True)
