import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import Post
from scraping_functions import login, get_posts

'''
username = ''
password = ''
profile = ''
'''


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, metavar='',
                        help='Username that will be used to access the Twitter account')
    parser.add_argument('-p', '--password', type=str, metavar='',
                        help='Password of the Username that will be used access the Twitter account')
    parser.add_argument('-q', '--query', type=str, metavar='', help='Query to be searched on Instagram')
    parser.add_argument('-n', '--num_posts', type=int, metavar='', default=3,
                        help='Number of posts to scrape starting from the most recent one')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # service = Service('/snap/bin/chromedriver')
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # browser = webdriver.Chrome(service, options=options)
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)

    if not login(args, browser):
        print("Login failed")
        return
    print("Login successful")

    path = '{}_crawl.json'.format(args.query)
    try:
        json_file, data = open_or_create_json(path)

        if data:
            posts_url = data[-1]['page_url']
        else:
            json_file.write('[')
            posts_url = 'https://mbasic.facebook.com/' + args.query + '?v=timeline'
        posts = []
        posts_to_find = args.num_posts
        # Dummy function
        # full_url = 'https://mbasic.facebook.com/' + profile

        profile_url = 'https://mbasic.facebook.com/' + args.query
        '''get_profile_info(profile_url, browser)'''

        print(posts_url)
        get_posts(posts_url, posts_to_find, browser, posts, json_file)
    finally:
        print('Closing File...')
        json_file.write(']')
        json_file.close()
        browser.quit()

def open_or_create_json(path):
    try:
        json_file = open(path, 'r+', encoding='utf-8')
        data = json.load(json_file)
        return json_file, data

    except IOError:
        print('File not found, will create a new one.')
        # Create file
        json_file = open(path, 'w', encoding='utf-8')
        data = None
        return json_file, data



# TODO:
#  1. Move recursively to the next pages by pressing 'See More Stories'
#  2. Retrieve comments from each post and their replies
#  3. Save the content as dict in a .json file as per other crawlers



if __name__ == '__main__':
    main()
