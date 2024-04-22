from instagrapi import Client
import json
import time
from datetime import datetime, timezone
from cachetools import TTLCache
from .exceptions.exceptions import WrongDateString


class InstaPosts:
    cache = TTLCache(maxsize=10000, ttl=3600)

    def __init__(self, username: str, password: str, query: str, reels: bool = False, tag: bool = False, hashtag: str = 'none',
                 recent_hash: int = -1, top_hash: int = -1, until: str = 'none', since: str = 'none', num_posts: int = 10,
                 comments: int = 0, likers: bool = False, bio: bool = False, followers: int = -1, following: int = -1, story: int = -1):

        print("[ig_postget]: You or your program started InstaPostget")
        # Parameters initialization
        self.username = username
        self.password = password
        self.query = query
        self.reels = reels
        self.tag = tag
        self.hashtag = hashtag
        self.recent_hash = recent_hash
        self.top_hash = top_hash
        self.until = until
        self.since = since
        self.num_posts = num_posts
        self.comments = comments
        self.likers = likers
        self.bio = bio
        self.followers = followers
        self.following = following
        self.story = story

        # Check if date format is correct if inserted any
        try:
            self.check_date()
        except WrongDateString as e:
            print(f'[ig_postget]: {e}')
            print('           Ignoring since and until parameters since one among them was set wrong')
            self.since = 'none'
            self.until = 'none'
            print(
                f'           Setting them back to default values to ignore them: since = {self.since}, until = {self.until}')

        # Initialization of dictionary
        self.results = {}
        self.medias = {}
        self.hashtags = []

        # Initialization of instagrapi
        print("[ig_postget]: Initializing client")
        self.cl = Client()
        self.cl.login(self.username, self.password)
        time.sleep(3)
        self.user_id = self.cl.user_id_from_username(self.query)

    def get_media(self, amount: int):
        print("[ig_postget]: Initializing cache")
        cache_key = f"{self.user_id}_{amount}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        print("[ig_postget]: Retrieving media")
        if self.reels:
            self.medias = self.cl.user_clips(self.user_id, amount)
        elif self.tag:
            self.medias = self.cl.usertag_medias(self.user_id, amount)
        else:
            self.medias = self.cl.user_medias(self.user_id, amount)

        self.results["media"] = self.medias
        self.cache[cache_key] = self.results

    def fetch_all(self):
        total_media = self.cl.user_info(self.user_id).media_count
        self.get_media(total_media)

    def get_hashtag(self):
        print("[ig_postget]: Researching hashtags")
        self.hashtags = self.cl.hashtag_info(self.hashtag)
        if self.recent_hash != -1:
            self.medias["recent_hashtag"] = self.cl.hashtag_medias_recent(self.hashtag, self.recent_hash)
        if self.top_hash != -1:
            self.medias["top_hashtag"] = self.cl.hashtag_medias_top(self.hashtag, self.top_hash)

    def check_date(self):
        if self.since != 'none':
            try:
                self.since = datetime.strptime(self.since, "%Y-%m-%d")
            except ValueError:
                raise WrongDateString(self.since, 'YYYY-MM-DD')

        if self.until != 'none':
            try:
                self.until = datetime.strptime(self.until, "%Y-%m-%d")
            except ValueError:
                raise WrongDateString(self.until, 'YYYY-MM-DD')

    def timeframe(self):
        print("[ig_postget]: Retrieving media in provided timeframe")
        if self.since or self.until:
            self.fetch_all()
        time.sleep(5)
        filtered_medias = {}
        for category, medias in self.medias.items():
            filtered_list = [
                media for media in medias if self.is_within_timeframe(media.taken_at.replace(tzinfo=timezone.utc))
            ]
            if filtered_list:
                filtered_medias[category] = filtered_list

        self.medias = filtered_medias

    def is_within_timeframe(self, media_date):
        if self.since and self.until:
            return self.since <= media_date <= self.until
        elif self.since:
            return media_date >= self.since
        elif self.until:
            return media_date <= self.until
        return True

    def fetch_post_data(self):
        print("[ig_postget]: Retrieving post data")
        self.results["comments"] = {}
        for media in self.medias:
            media_dict = media.dict()
            comments = self.cl.media_comments(media.id, self.comments)
            comments_data = [comment.dict() for comment in comments]
            media_dict["comments"] = comments_data
            time.sleep(1)
            if self.likers:
                likes = self.cl.media_likers(media.id)
                likes_data = [user.dict() for user in likes]
                media_dict["likers"] = likes_data
            self.results["media"].append(media_dict)

    def get_bio(self):
        print("[ig_postget]: Retrieving bio")
        if self.bio:
            self.results["bio"] = []
            user_bio = self.cl.user_info(self.user_id)
            self.results["bio"].append(user_bio.dict())

    def get_followers(self):
        print("[ig_postget]: Retrieving list of followers")
        if self.followers != -1:
            self.results["followers"] = self.cl.user_followers(self.user_id, True, self.followers)

    def get_following(self):
        print("[ig_postget]: Retrieving list of following")
        if self.following != -1:
            self.results["followers"] = self.cl.user_followers(self.user_id, True, self.following)

    def get_story(self):
        print("[ig_postget]: Retrieving stories of user")
        if self.story != -1:
            self.results["story"] = []
            stories = self.cl.user_stories(self.user_id, self.story)
            for story in stories:
                story_dict = story.dict()
                self.results["story"].append(story_dict)

    def save(self):
        print("[ig_postget]: Saving parsed data in .json")
        json_data = json.dumps(self.results, indent=4, default=str)
        with open('ig_crawled_bio.json', 'w') as json_file:
            json_file.write(json_data)
        print("Data has been written to .json")

    def clear_media(self):
        self.results = {}
        self.medias = {}

    def logout(self):
        print("[ig_postget]: logging out")
        self.cl.logout()
