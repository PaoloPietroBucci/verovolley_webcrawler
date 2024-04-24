import json
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# python3 main.py --username *** --password *** --query https://www.linkedin.com/in/justinwelsh/
# python3 main.py --username *** --password *** --query https://www.linkedin.com/in/justinwelsh/ --numposts 20

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, metavar='',
                        help='Username that will be used to access the Twitter account')
    parser.add_argument('--password', type=str, metavar='',
                        help='Password of the Username that will be used access the Twitter account')
    parser.add_argument('--query', type=str, metavar='', help='Query to be searched on Instagram')
    # parser.add_argument('--until', type=str, metavar='YYYY-MM-DD', default=None,
    #                     help='String of the date until which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    # parser.add_argument('--since', type=str, metavar='YYYY-MM-DD', default=None,
    #                     help='String of the date from which the posts will be returned. Format: YYYY-MM-DD, UTC time.')
    parser.add_argument('-np', '--numposts', type=int, metavar='', default=3,
                        help='Number of posts to scrape starting from the most recent one')
    # parser.add_argument('--comments', type=int, metavar='', default=0,
    #                     help='Number of comments to scrape from each post')
    # parser.add_argument('--reels', action='store_true', help='Call with this if you want get list of only reels')
    # parser.add_argument('--tag', action='store_true',
    #                     help='Call with this if you want get list of only the posts the user was tagged in')
    # parser.add_argument('--likers', action='store_true',
    #                     help='Call with this if you also want get list of users who liked the post (due to Instagram limitations, this may not return a complete list)')
    # parser.add_argument('--followers', action='store_true',
    #                     help='Call with this if you also want get a list of users who followers the user')
    # parser.add_argument('--numfollowers', type=int, metavar='', default=10,
    #                     help='Number of followers you want to return')
    # parser.add_argument('--following', action='store_true',
    #                     help='Call with this if you also want get a list of users who the user follows')
    # parser.add_argument('--numfollowing', type=int, metavar='', default=10,
    #                     help='Number of following you want to return')
    # parser.add_argument('--story', action='store_true',
    #                     help='Call with this if you also want get a list of stories published by the user')
    # parser.add_argument('--numstory', type=int, metavar='', default=1,
    #                     help='Number of stories published by the user to return')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    service = Service('/snap/bin/chromium.chromedriver')
    options = Options()
    options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(service=service, options=options)
    browser.implicitly_wait(10)

    if not login(args, browser):
        print("Login failed")
        return

    print("Login successful")

    profile = get_profile(args.query, browser)
    posts = get_profile_posts(args.query, browser, args.numposts)
    profile_posts = combine_data(json.loads(profile), json.loads(posts))
    save_to_json(profile_posts)

    browser.quit()


def login(args, browser):
    # get the cookies from the last session
    browser.get('https://www.linkedin.com')
    try:
        with open('last_cookies.json', 'r') as json_file:
            cookies = json.load(json_file)
            for cookie in cookies:
                browser.add_cookie(cookie)
            return True
    except FileNotFoundError:
        pass

    browser.get('https://www.linkedin.com/login')
    sleep(2)

    browser.find_element(By.ID, 'username').send_keys(args.username)
    browser.find_element(By.ID, 'password').send_keys(args.password)
    browser.find_element(By.CSS_SELECTOR, '.login__form_action_container button').click()

    if browser.current_url.startswith('https://www.linkedin.com/checkpoint/challenge'):
        remaining_time = 60
        while remaining_time > 0:
            if browser.current_url.startswith('https://www.linkedin.com/feed/'):
                break
            print(f'\rTime remaining to complete the challenge: {remaining_time} seconds', end='')
            sleep(1)
            remaining_time -= 1
        print('\r', end='')
        if remaining_time == 0:
            return False
    sleep(2)
    cookies = browser.get_cookies()
    data = json.dumps(cookies, ensure_ascii=False, indent=4).encode('utf-8')
    with open('last_cookies.json', 'w') as json_file:
        json_file.write(data)
    return True


# def get_company(args, browser: WebDriver):
#     browser.get(args.query + 'posts/?feedView=all')
#     sleep(2)
#
#     # Get the page source
#     page_source = browser.page_source  # Parse the HTML using Beautiful Soup
#     soup = BeautifulSoup(page_source, 'html.parser')  # Extract the name and headline
#     name = soup.find('h1',
#                      class_='ember-view org-top-card-summary__title text-display-medium-bold full-width').text.strip()
#     print('Name:', name)
#     posts = soup.find_all('div', class_='ember-view occludable-update')
#     for post in posts:
#         post_text = post.find('span', class_='break-words').span.text.strip()
#
#         buttons = browser.find_elements(By.CSS_SELECTOR, '.social-details-social-counts__comments')
#         print(buttons)
#         for button in buttons:
#             button.click()
#             sleep(5)
#             comments = browser.find_elements(By.CSS_SELECTOR, '.update-components-text .relative')
#             for comment in comments:
#                 print(comment.text)
#         print(post_text)
#     return soup


def get_profile(profile_url: str, browser: WebDriver) -> bytes:
    browser.get(profile_url)
    sleep(2)

    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    name = soup.find('h1',
                     class_='text-heading-xlarge inline t-24 v-align-middle break-words').text.strip()
    header = soup.find('div', class_='text-body-medium break-words').text.strip()
    location = soup.find('span', class_='text-body-small inline t-black--light break-words').text.strip()
    about_section = soup.find('section', class_='artdeco-card pv-profile-card break-words mt2')
    about = about_section.find('div', class_='display-flex ph5 pv3').div.div.div.span.text.strip()
    return json.dumps({'name': name, 'header': header, 'location': location, 'about': about}, ensure_ascii=False, indent=4).encode('utf-8')


def get_profile_posts(profile_url: str, browser: WebDriver, num_posts: int) -> bytes:
    browser.get(profile_url + 'recent-activity/all/')
    sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    posts = soup.find_all('li', class_='profile-creator-shared-feed-update__container')
    scrolls = 1
    while len(posts) < num_posts + 20:
        scroll_height = f"window.scrollTo(0, {1080 * scrolls});"
        browser.execute_script(scroll_height)
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        posts = soup.find_all('li', class_='profile-creator-shared-feed-update__container')
        scrolls += 1
    sleep(2)

    comments_buttons = browser.find_elements(By.CSS_SELECTOR, '.comment-button')
    comments_buttons = comments_buttons[:num_posts]
    for button in comments_buttons:
        try:
            button.click()
        except Exception:
            pass
        sleep(1)
    sleep(2)

    more_comments_buttons = browser.find_elements(By.CSS_SELECTOR,
                                                  '.comments-comments-list__load-more-comments-button')
    more_comments_buttons = more_comments_buttons[:num_posts]
    for button in more_comments_buttons:
        try:
            button.click()
        except Exception:
            pass
        sleep(1)
    sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    posts = soup.find_all('li', class_='profile-creator-shared-feed-update__container')[:num_posts]
    json_posts = []
    for post in posts:
        try:
            post_text = post.find('span', class_='break-words').span.text.strip()
            json_posts.append({'post': post_text, 'comments': []})
            comments = post.find_all('article', 'comments-comment-item comments-comments-list__comment-item')
            for comment in comments:
                comment_author = comment.find('span',
                                              class_='comments-post-meta__name-text hoverable-link-text mr1').span.span.text.strip()
                comment_text = comment.find('div', class_='update-components-text relative').span.text.strip()
                json_posts[-1]['comments'].append({'author': comment_author, 'comment': comment_text})
        except AttributeError:
            pass
    return json.dumps(json_posts, ensure_ascii=False, indent=4).encode('utf-8')


def combine_data(profile_data, posts_data) -> bytes:
    profile_data['posts'] = posts_data
    return json.dumps(profile_data, ensure_ascii=False, indent=4).encode('utf-8')


def save_to_json(data):
    with open('linkedin_crawled_example.json', 'w') as json_file:
        json_file.write(data.decode('utf-8'))
    print("Data has been written to .json")


if __name__ == '__main__':
    main()
