import json
from instagrapi import Client

account_username = 'mihenetrunis'
account_password = 'mihenetrunis123'
account_toscrape = 'verovolley'

num_of_posts = 3
num_of_comments = 5


def main():
    cl = Client()
    cl.login(account_username, account_password)

    user_id = cl.user_id_from_username(account_toscrape)
    medias = cl.user_medias(user_id, num_of_posts)

    # Save to a json file
    results = {}
    results["media"] = []
    # Loop through each media to fetch comments
    results["comments"] = {}
    for media in medias:
        media_dict = media.dict()
        comments = cl.media_comments(media.id, num_of_comments)
        comments_data = [comment.dict() for comment in comments]
        media_dict["comments"] = comments_data
        results["media"].append(media_dict)

    json_data = json.dumps(results, indent=4, default=str)
    with open('ig_crawled.json', 'w') as json_file:
        json_file.write(json_data)

    print("Data has been written to test.json")


if __name__ == '__main__':
    main()
