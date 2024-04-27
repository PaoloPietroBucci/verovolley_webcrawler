from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
import os

logger = logging.getLogger()


class InstaPosts:
    def __init__(self, username: str, password: str, query: str, hashtag: str, reels: bool = False, tag: bool = False,
                 recent_hash: int = -1, top_hash: int = -1, num_posts: int = 3, comments: int = 0, likers: bool = False,
                 bio: bool = False, followers: int = -1, following: int = -1, story: int = -1):

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
        self.num_posts = num_posts
        self.comments = comments
        self.likers = likers
        self.bio = bio
        self.followers = followers
        self.following = following
        self.story = story

        # Initialization of dictionary
        self.results = {}
        self.medias = []
        self.hashtag_info = None

        # Initialization of instagrapi
        print("[ig_postget]: Initializing client")
        self.cl = Client()
        self.login_user()
        self.cl.delay_range = [1, 3]
        self.user_id = None

    def login_user(self):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        path = "ig_postget/session.json"
        if os.path.exists(path):
            session = self.cl.load_settings(path)

            login_via_session = False
            login_via_pw = False

            if session:
                try:
                    self.cl.set_settings(session)
                    self.cl.login(self.username, self.password)

                    # check if session is valid
                    try:
                        self.cl.get_timeline_feed()
                    except LoginRequired:
                        logger.info("[ig_postget]: Session is invalid, need to login via username and password")

                        old_session = self.cl.get_settings()

                        # use the same device uuids across logins
                        self.cl.set_settings({})
                        self.cl.set_uuids(old_session["uuids"])

                        self.cl.login(self.username, self.password)
                    login_via_session = True
                except Exception as e:
                    logger.info("[ig_postget]: Couldn't login user using session information: %s" % e)

            if not login_via_session:
                try:
                    logger.info("[ig_postget]: Attempting to login via username and password. username: %s" % self.username)
                    if self.cl.login(self.username, self.password):
                        login_via_pw = True
                except Exception as e:
                    logger.info("[ig_postget]: Couldn't login user using username and password: %s" % e)

            if not login_via_pw and not login_via_session:
                raise Exception("[ig_postget]: Couldn't login user with either password or session")
        else:
            self.cl.login(self.username, self.password)
            self.cl.dump_settings(path)

    def get_media(self, amount: int):
        self.user_id = self.cl.user_id_from_username(self.query)
        if self.reels:
            print("[ig_postget]: Retrieving reel media type")
            self.medias = self.cl.user_clips(self.user_id, amount)
        elif self.tag:
            print("[ig_postget]: Retrieving tag media type")
            self.medias = self.cl.usertag_medias(self.user_id, amount)
        else:
            print("[ig_postget]: Retrieving all media type")
            self.medias= self.cl.user_medias(self.user_id, amount)

    def get_hashtag(self):
        print("[ig_postget]: Researching hashtags")
        self.hashtag_info = self.cl.hashtag_info(self.hashtag)
        if self.recent_hash != -1:
            self.medias = self.cl.hashtag_medias_recent(self.hashtag, self.recent_hash)
        if self.top_hash != -1:
            self.medias = self.cl.hashtag_medias_top(self.hashtag, self.top_hash)

    def fetch_post_data(self):
        print("[ig_postget]: Retrieving post data")
        self.results["media"] = []
        self.results["hashtag"] = []
        if self.hashtag:
            self.results["hashtag"].append(self.hashtag_info.dict())
        for media in self.medias:
            media_dict = media.dict()
            comments = self.cl.media_comments(media.id, self.comments)
            comments_data = [comment.dict() for comment in comments]
            media_dict["comments"] = comments_data
            if self.likers:
                likes = self.cl.media_likers(media.id)
                likes_data = [user.dict() for user in likes]
                media_dict["likers"] = likes_data
            self.results["media"].append(media_dict)

    def get_bio(self):
        if self.bio:
            print("[ig_postget]: Retrieving bio")
            self.results["bio"] = []
            user_bio = self.cl.user_info(self.user_id)
            self.results["bio"].append(user_bio.dict())

    def get_followers(self):
        if self.followers != -1:
            print("[ig_postget]: Retrieving list of followers")
            self.results["followers"] = self.cl.user_followers(self.user_id, True, self.followers)

    def get_following(self):
        if self.following != -1:
            print("[ig_postget]: Retrieving list of following")
            self.results["following"] = self.cl.user_following(self.user_id, True, self.following)

    def get_story(self):
        if self.story != -1:
            print("[ig_postget]: Retrieving stories of user")
            self.results["story"] = []
            stories = self.cl.user_stories(self.user_id, self.story)
            for story in stories:
                story_dict = story.dict()
                self.results["story"].append(story_dict)

    def save(self):
        print("[ig_postget]: Saving parsed data in .json")
        json_data = json.dumps(self.results, indent=4, default=str, ensure_ascii=False)
        with open('ig_crawled.json', 'w') as json_file:
            json_file.write(json_data)
        print("[ig_postget]: Data has been written to .json")

    def clear_media(self):
        self.results = {}
        self.medias = []

    def logout(self):
        print("[ig_postget]: logging out")
        self.cl.logout()
