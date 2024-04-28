import json
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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

    # Dummy function
    full_url = 'https://mbasic.facebook.com/' + args.query
    # full_url = 'https://mbasic.facebook.com/' + profile
    get_profile_info(full_url, browser)
    get_posts(full_url, args.num_posts, browser)
    browser.quit()


def login(args, browser):
    browser.get('https://mbasic.facebook.com/login')
    try:  # Get the cookies from the last session
        with open('session.json', 'r') as json_file:
            cookies = json.load(json_file)
            for cookie in cookies:
                browser.add_cookie(cookie)
            return True
    except FileNotFoundError:
        pass

    sleep(2)
    browser.find_element(By.CSS_SELECTOR, '.br').click()  # Accept cookies
    sleep(2)
    # browser.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(username)
    browser.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(args.username)
    # browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]').send_keys(password)
    browser.find_element(By.CSS_SELECTOR, 'input[name="pass"]').send_keys(args.password)
    browser.find_element(By.CSS_SELECTOR, 'input[name="login"]').click()
    sleep(2)
    browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()  # Accept prompt
    sleep(2)

    cookies = browser.get_cookies()
    session = json.dumps(cookies, indent=4)
    with open('session.json', 'w') as json_file:
        json_file.write(session)

    return True


# currently the get_profile_Info() is suited only on the content of 'verovolley'
# TODO: change the soup.find() so it can work with any passed profile.
#  One was to do it is to find ALL the possible option available by facebook during the creation of a profile,
#  and check if the option is present in the current profile managing it accordingly:
#  1. If present > save the content
#  2. If not present > save None in the json
def get_profile_info(profile_url: str, browser: WebDriver):
    browser.get(profile_url)
    source_data = browser.page_source
    soup = BeautifulSoup(source_data, 'html.parser')

    profile_cover_photo_container = soup.find(id="profile_cover_photo_container").find('img')['src']
    profile_picture = soup.find('img', class_="ca r")['src']
    name_of_profile = soup.find('strong', class_="cc").text.strip()
    bio_of_profile = soup.find('div', class_="cj ck cl cm").text.strip()
    id_category_content = soup.find('div', id="category").find('span', class_="ci").text.strip()

    contact_info_section = soup.find(id="contact-info")
    address = contact_info_section.find('a').text.strip()
    facebook = contact_info_section.find_all('div', class_="ds")[1].text.strip()
    websites = contact_info_section.find_all('div', class_="ds")[2].find('a')['href']

    id_bio_content = soup.find(id="bio").find('div', class_="dk dl dm").text.strip()

    year_overviews_section = soup.find(id="year-overviews")
    year_overviews_content = []
    if year_overviews_section:
        year_events = year_overviews_section.find_all('div')
        for event in year_events:
            if event.text.strip():
                year_overviews_content.append(event.text.strip())
    if not year_overviews_content:
        year_overviews_content = "No specific events listed."

    profile_info = {'profile_cover_photo': profile_cover_photo_container, 'profile_picture': profile_picture,
                    'profile_name': name_of_profile, 'bio': bio_of_profile, 'category': id_category_content,
                    'address': address, 'facebook': facebook, 'websites': websites, 'about': id_bio_content,
                    'life_events': year_overviews_content}

    json_info = json.dumps(profile_info, ensure_ascii=False, indent=4)

    with open("profile_info.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_info)


# TODO:
#  1. Move recursively to the next pages by pressing 'See More Stories'
#  2. Retrieve comments from each post and their replies
#  3. Save the content as dict in a .json file as per other crawlers
def get_posts(posts_url: str, num_posts: int, browser: WebDriver) -> list[dict]:
    full_url = posts_url + '?v=timeline'
    browser.get(full_url)

    soup = BeautifulSoup(browser.page_source, 'html.parser')  # Can be used to go to the next page
    sleep(5)

    # To be returned
    posts = []
    post_count = 0

    while post_count < num_posts:
        # Get HTML elements
        crawled_posts = browser.find_elements(By.TAG_NAME, 'article')
        for crawled_post in crawled_posts:
            # Get post content
            paragraphs = crawled_post.find_elements(By.TAG_NAME, 'p')
            text = []
            for paragraph in paragraphs:
                text.append(paragraph.get_attribute('textContent').strip())
            post_content = "".join(text)

            # Get post likes
            footer_element = crawled_post.find_element(By.TAG_NAME, 'footer').find_element(By.TAG_NAME, 'a')
            likes = footer_element.text
            # If there's no likes this text should be just "Like"
            if any(char.isdigit() for char in likes):
                num_likes = likes.split(' ')[0]
            else:
                num_likes = 0

            # Get number of comments
            footer = crawled_post.find_element(By.TAG_NAME, 'footer').find_elements(By.TAG_NAME, 'a')
            comments = footer[3].text
            # If there's no comments this text should be just "Comment"
            if any(char.isdigit() for char in comments):
                num_comments = comments.split(' ')[0]
            else:
                num_comments = 0

            posts.append({
                'content': post_content,
                'num_likes': num_likes,
                'num_comments': num_comments,
            })
            post_count = post_count + 1

            # TODO: Go to next page of posts
            # next_page = soup.find('td', class_="u")
            # Click link of next page
            #   next.page.click()
        print(posts)
        # Return if we have reached the desired number of posts
    return posts


if __name__ == '__main__':
    main()
