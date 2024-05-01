import json
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import Post
from facebook.scraping_functions import get_comments, get_profile_info, login, get_posts

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

    posts = []
    posts_to_find = args.num_posts
    # Dummy function
    # full_url = 'https://mbasic.facebook.com/' + profile

    profile_url = 'https://mbasic.facebook.com/' + args.query
    '''get_profile_info(profile_url, browser)'''

    posts_url = 'https://mbasic.facebook.com/' + args.query + '?v=timeline'
    get_posts(posts_url, posts_to_find, browser, posts)

    browser.quit()
    path = 'facebook_crowl.json'
    with open(path, 'w', encoding='utf-8') as file_json:
        json.dump(posts, file_json, indent=4, ensure_ascii=False)


# TODO:
#  1. Move recursively to the next pages by pressing 'See More Stories'
#  2. Retrieve comments from each post and their replies
#  3. Save the content as dict in a .json file as per other crawlers



if __name__ == '__main__':
    main()
