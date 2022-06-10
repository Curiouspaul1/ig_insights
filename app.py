from insights import Insights
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

nxt, client = None, None


@app.get('/')
def get_hashtag_posts():
    global client
    global nxt
    print(request.args.get('hashtag'))
    client = Insights(
        os.getenv('user_id'),
        os.getenv('access_token'),
        request.args.get('hashtag')
    )
    data = client.fetch_hashtag_posts()
    nxt = data['paging']['cursors']['after']
    print(data['paging']['cursors'])
    return jsonify(
       data['data']
    )


@app.get('/next')
def fetch_next():
    global client
    global nxt

    data = client.fetch_hashtag_posts(after=nxt)

    print(nxt, end="\n")

    nxt = data['paging']['cursors']['after']

    return jsonify(
        data['data']
    )

app.run(debug=True)
