import json


class Post:

    def __init__(self, content, num_comments, date, likes_num, comments: []):
        self.content = content
        self.author = num_comments
        self.likes_num = likes_num
        self.comments = comments
        self.date = date

    def write_to_file(self, dest_file):
        json.dump(self.__json__(), dest_file, indent=4, ensure_ascii=False)

    def __json__(self):
        return {
            'content' : self.content,
            'author': self.author,
            'date' : self.date,
            'likes_num': self.likes_num,
            'comments': self.comments
        }

class Comments:

    def __init__(self, author, num_likes, body, date):
        self.author = author
        self.num_likes = num_likes
        self.body = body

