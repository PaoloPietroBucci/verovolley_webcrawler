from instagrapi import Client
import json
import argparse
from datetime import datetime

# python3 main.py --username laconraffael --password qwerty123lacon --query verovolley

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, metavar='',
                        help='Username that will be used to access the Twitter account')
    parser.add_argument('--password', type=str, metavar='',
                        help='Password of the Username that will be used access the Twitter account')
    parser.add_argument('--query', type=str, metavar='', help='Query to be searched on Instagram')
    parser.add_argument('--until', type=str, metavar='YYYY-MM-DD', default=None,
                        help='String of the date until which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    parser.add_argument('--since', type=str, metavar='YYYY-MM-DD', default=None,
                        help='String of the date from which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    parser.add_argument('-np', '--numposts', type=int, metavar='', default=3,
                        help='Number of posts to scrape starting from the most recent one')
    parser.add_argument('--comments', type=int, metavar='', default=0,
                        help='Number of comments to scrape from each post')
    parser.add_argument('--reels', action='store_true', help='Call with this if you want get list of only reels')
    parser.add_argument('--tag', action='store_true', help='Call with this if you want get list of only the posts the user was tagged in')

    args = parser.parse_args()
    return args


# TODO: filter the media by date
'''
def filter_media_by_date(medias, since=None, until=None):
    if not since and not until:
        return medias

    filtered_posts = []
    for m in medias:
        post_date = m.taken_at.date()
        if since and post_date < datetime.strptime(since, '%Y-%m-%d').date():
            continue
        if until and post_date > datetime.strptime(until, '%Y-%m-%d').date():
            continue
        filtered_posts.append(m)
    return filtered_posts
'''

def main():
    args = parse_args()
    cl = Client()
    cl.login(args.username, args.password)

    user_id = cl.user_id_from_username(args.query)
    # Select media type (all or only reels)
    if args.reels:
        medias = cl.user_clips(user_id, args.numposts)
    elif args.tag:
        medias = cl.usertag_medias(user_id, args.numposts)
    else:
        medias = cl.user_medias(user_id, args.numposts)

    # Filter medias by date, if specified
    # medias = filter_media_by_date(medias, args.since, args.until)

    # Save to a json file
    results = {}
    results["media"] = []
    # Loop through each media to fetch comments
    results["comments"] = {}
    for media in medias:
        media_dict = media.dict()
        comments = cl.media_comments(media.id, args.comments)
        comments_data = [comment.dict() for comment in comments]
        media_dict["comments"] = comments_data
        results["media"].append(media_dict)

    json_data = json.dumps(results, indent=4, default=str)
    with open('ig_crawled.json', 'w') as json_file:
        json_file.write(json_data)
    print("Data has been written to .json")

    cl.logout()


if __name__ == '__main__':
    main()
