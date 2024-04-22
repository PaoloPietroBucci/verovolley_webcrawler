import argparse
from ig_postget.posts import InstaPosts

# python3 main.py --username tihadina3 --password 123tihadina3 --query verovolley


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, metavar='',
                        help='Username that will be used to access the Instagram account')
    parser.add_argument('-p', '--password', type=str, metavar='',
                        help='Password of the Username that will be used access the Instagram account')
    parser.add_argument('-q', '--query', type=str, metavar='',
                        help='Query to be searched on Instagram')
    parser.add_argument('-r', '--reels', action='store_true',
                        help='Call with this if you want get list of only reels')
    parser.add_argument('-t', '--tag', action='store_true',
                        help='Call with this if you want get list of only the posts the user was tagged in')
    parser.add_argument('-h', '--hashtag', type=str, metavar='',
                        help='Hashtag to be searched on Instagram. With a list of related hashtags')
    parser.add_argument('-rh', '--recent_hash', type=int, metavar='', default=10,
                        help='Return the selected amount of most recent posts by hashtag')
    parser.add_argument('-th', '--top_hash', type=int, metavar='', default=10,
                        help='Return the selected amount of top posts by hashtag')
    parser.add_argument('--until', type=str, metavar='YYYY-MM-DD', default=None,
                        help='String of the date until which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    parser.add_argument('--since', type=str, metavar='YYYY-MM-DD', default=None,
                        help='String of the date from which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    parser.add_argument('-np', '--num_posts', type=int, metavar='', default=3,
                        help='Number of posts to scrape starting from the most recent one')
    parser.add_argument('-c', '--comments', type=int, metavar='', default=0,
                        help='Number of comments to scrape from each post. 0 means all the comments')
    parser.add_argument('--likers', action='store_true',
                        help='Call with this if you also want get list of users who liked the post (due to Instagram limitations, this may not return a complete list)')
    parser.add_argument('--bio', action='store_true',
                        help='Call with this if you also want get the bio of the user you are searching for')
    parser.add_argument('--followers', type=int, metavar='', default=10,
                        help='Call with this if you also want get a list of the amount of users who followers the user')
    parser.add_argument('--following', type=int, metavar='', default=10,
                        help='Call with this if you also want get a list of the amount of users who the user follows')
    parser.add_argument('--story', type=int, metavar='', default=1,
                        help='Call with this if you also want get a list of the amount of stories published by the user')
    try:
        args = parser.parse_args()
        return args
    except argparse.ArgumentError:
        parser.print_help()
    exit()


def main():
    args = parse_args()

    ig_getter = InstaPosts(args.username, args.password, args.query, args.reels, args.tag, args.hashtag, args.recent_hash,
                           args.top_hash, args.until, args.since, args.num_posts, args.comments, args.likers, args.bio,
                           args.followers, args.following, args.story)

    print("Retrieving posts from Instagram")
    ig_getter.get_media(args.num_posts)
    ig_getter.get_hashtag()

    ig_getter.check_date()
    ig_getter.timeframe()

    ig_getter.fetch_post_data()

    ig_getter.get_bio()
    ig_getter.get_followers()
    ig_getter.get_following()
    ig_getter.get_story()

    ig_getter.save()

    print("Clearing Media")
    ig_getter.clear_media()
    ig_getter.logout()


if __name__ == '__main__':
    main()
