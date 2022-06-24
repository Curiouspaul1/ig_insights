import requests
import os
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

# URL = "https://graph.facebook.com/v14.0"

# def fetch_hashtag_id(hashtag, user_id):
#     res = requests.get(f"{URL}/ig_hashtag_search?user_id={user_id}&q={hashtag}&access_token={os.getenv('access_token')}")
#     return res.json()

# def display_posts(hashtag, user_id):
#     hashtag_id = fetch_hashtag_id(hashtag, user_id)['data'][0].get('id')
#     print(hashtag_id)
#     res = requests.get(f"{URL}/{hashtag_id}/recent_media?user_id={user_id}&access_token={os.getenv('access_token')}")
#     return res.json()


# print(display_posts("apple", os.getenv('user_id')))




class Insights:
    BASE_URL = "https://graph.facebook.com/v14.0"

    def __init__(self, user_id, token, hashtag, endpoint):
        self.user_id = user_id
        self.token = token
        self.hashtag = hashtag
        self.endpoint = endpoint
    
    def append_params(self, url, params: Optional[str] = None):
        url = url+f"?user_id={self.user_id}&access_token={self.token}"
        if params:
            for k, v in params.items():
                url+=f"&{k}={v}"
        return url
    
    def fetch_hashtag_id(self):
        params = {
            'q': self.hashtag
        }
        _id = requests.get(
            url=self.append_params(f"{Insights.BASE_URL}/ig_hashtag_search", params)
        )
        if _id.status_code == 200:
            return _id.json().get('data')[0].get('id')
        print(_id.json())
        return None
    
    def fetch_hashtag_posts(self, hashtag_id: Optional[str] = None, after: Optional[str]=None):
        params = {
            'fields': 'like_count,id,comments_count,media_type,media_url,permalink',
            'pretty': 0
        }
        if after:
            params['after'] = after
        if not hashtag_id:
            hashtag_id = self.fetch_hashtag_id()
        if hashtag_id:
            posts = requests.get(
                url=self.append_params(f"{Insights.BASE_URL}/{hashtag_id}/{self.endpoint}", params)
            )
            if posts.status_code == 200:
                return posts.json()
            print(posts.json())
            return None
    # else:
        #     posts = requests.get(
        #         url=self.append_params(f"{Insights.BASE_URL}/{_id}/recent_media")
        #     )
        #     if posts.status_code == 200:
        #         return posts.json()
        #     print(posts.json())
        #     return None
    
    # def post_insight(self, post):
    #     params = {
    #         'metric': 'impressions,reach,engagement'
    #     }
    #     res = requests.get(
    #         url=f"{self.append_params('{}/{}/insights'.format(Insights.BASE_URL, post))}"
    #     )
    #     print(f"{self.append_params('{}/{}/insights'.format(Insights.BASE_URL, post))}")
    #     if res.status_code == 200:
    #         return res.json()
    #     print(res.json())
    
    # def fetch_posts_insight(self, posts: Optional[List] = None):
    #     if not posts:
    #         posts = self.fetch_hashtag_posts(self.hashtag)
    #     return posts
            