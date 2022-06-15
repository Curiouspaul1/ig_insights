from insights import Insights
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

nxt, client = None, None


def update_obj(obj):
    if obj['comments_count'] != 0:
        obj.update(
            {
                'like_comment_ratio':obj['like_count']/obj['comments_count']
            }
        )
    else:
        obj.update({
            'like_comment_ratio': None
        })
    return obj


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
    mods = map(
        update_obj,
        data
    )

    return jsonify(
        list(mods)
    )


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
