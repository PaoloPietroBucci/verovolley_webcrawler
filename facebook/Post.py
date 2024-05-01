import json


class Post:

    def __init__(self, title, author, likes_num, comments: []):
        self.title = title
        self.author = author
        self.likes_num = likes_num
        self.comments = comments

    def __toJson(self, dest_file):
        json.dumps(self, dest_file,  indent=4)


class Comments:

    def __init__(self, author, num_likes, text):
        self.author = author
        self.num_likes = num_likes
        self.text = text
