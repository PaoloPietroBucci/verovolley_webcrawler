import json
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, metavar='',
                        help='Username that will be used to access the Twitter account')
    parser.add_argument('--password', type=str, metavar='',
                        help='Password of the Username that will be used access the Twitter account')
    parser.add_argument('--query', type=str, metavar='', help='Query to be searched on Instagram')
    parser.add_argument('-np', '--numposts', type=int, metavar='', default=3,
                        help='Number of posts to scrape starting from the most recent one')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    #service = Service('/snap/bin/chromium.chromedriver')
    options = Options()
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)

    if not login(args, browser):
        print("Login failed")
        return

    print("Login successful")

    # Dummy function
    posts = get_posts(args.query, browser)

    browser.quit()


def login(args, browser):
    # Get the cookies from the last session
    browser.get('https://mbasic.facebook.com/login')
    try:
        with open('session.json', 'r') as json_file:
            cookies = json.load(json_file)
            for cookie in cookies:
                browser.add_cookie(cookie)
            return True
    except FileNotFoundError:
        pass


    #Go to log in page
    browser.get('https://mbasic.facebook.com/login')
    sleep(2)

    # Accept cookies
    browser.find_element(By.CSS_SELECTOR, '.br').click()
    sleep(2)

    # Provide loging credentials and log in
    browser.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(args.username)
    browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]').send_keys(args.password)
    browser.find_element(By.CSS_SELECTOR, 'input[name="login"]').click()

    sleep(2)

    # Accept prompt
    browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    sleep(2)

    cookies = browser.get_cookies()
    session = json.dumps(cookies, indent=4)
    with open('session.json', 'w') as json_file:
        json_file.write(session)

    return True


# TODO: Definte this to get the timeline
def get_posts(posts_url: str, browser: WebDriver) -> bytes:
    browser.get('https://mbasic.facebook.com/' + 'verovolley')
    sleep(5)
    return None

if __name__ == '__main__':
    main()
