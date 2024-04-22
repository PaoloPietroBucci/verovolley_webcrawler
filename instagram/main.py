from instagrapi import Client
import json
import argparse
from datetime import datetime

# python3 main.py --username paolo.guf --password paolo.guf!123 --query verovolley
# python3 main.py --username insta_crow@yahoo.com --password crowler --query verovolley --followers --following
# python3 main.py --username paolo.guf --password paolo.guf!123 --query verovolley --story --numstory 1

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
    parser.add_argument('--likers', action='store_true',
                        help='Call with this if you also want get list of users who liked the post (due to Instagram limitations, this may not return a complete list)')
    parser.add_argument('--followers', action='store_true',
                        help='Call with this if you also want get a list of users who followers the user')
    parser.add_argument('--numfollowers', type=int, metavar='', default=10,
                        help='Number of followers you want to return')
    parser.add_argument('--following', action='store_true',
                        help='Call with this if you also want get a list of users who the user follows')
    parser.add_argument('--numfollowing', type=int, metavar='', default=10,
                        help='Number of following you want to return')
    parser.add_argument('--story', action='store_true',
                        help='Call with this if you also want get a list of stories published by the user')
    parser.add_argument('--numstory', type=int, metavar='', default=1,
                        help='Number of stories published by the user to return')
    parser.add_argument('--bio', action='store_true',
                        help='Call with this if you also want get the bio of the user you are searching for')

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
        # Inside the media_id save the list of likers
        if args.likers:
            likers = cl.media_likers(media.id)
            likers_data = [user.dict() for user in likers]
            media_dict["likers"] = likers_data
        results["media"].append(media_dict)

    if args.followers:
        if args.numfollowers:
            results["followers"] = cl.user_followers(user_id, True, args.numfollowers)
        else:
            results["followers"] = cl.user_followers(user_id, True, 0)
    if args.following:
        if args.numfollowing:
            results["following"] = cl.user_following(user_id, True, args.numfollowing)
        else:
            results["following"] = cl.user_following(user_id, True, 0)

    if args.story:
        results["story"] = []
        stories = cl.user_stories(user_id, args.numstory)
        for story in stories:
            story_dict = story.dict()
            results["story"].append(story_dict)

    if args.bio:
        results["bio"] = []
        user_bio = cl.user_info(user_id)
        results["bio"].append(user_bio.dict())

    json_data = json.dumps(results, indent=4, default=str)
    with open('ig_crawled_bio.json', 'w') as json_file:
        json_file.write(json_data)
    print("Data has been written to .json")

    cl.logout()


if __name__ == '__main__':
    main()
