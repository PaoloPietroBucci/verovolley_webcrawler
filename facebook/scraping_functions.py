import json
import argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml import etree


# currently the get_profile_Info() is suited only on the content of 'verovolley'
# TODO: change the soup.find() so it can work with any passed profile.
#  One was to do it is to find ALL the possible option available by facebook during the creation of a profile,
#  and check if the option is present in the current profile managing it accordingly:
#  1. If present > save the content
#  2. If not present > save None in the json

def get_posts(posts_url: str, num_posts: int, browser: WebDriver, posts_list: list, post_count=0):
    # To be returned
    print('Scraped post:', post_count)
    # do always
    browser.get(posts_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')  # Can be used to go to the next page
    next_page_link = None
    divs = soup.find('div', id="structured_composer_async_container").findChildren('div')
    for div in divs:
        print(div)
        if 'See more stories' in div.text:
            next_page_link = div.find('a').get('href')
    sleep(2)
    # Termination condition
    if post_count >= num_posts:
        return
    else:
        posts = soup.find('section').find_all('article')
        for post in posts:
            # Get post content
            paragraphs = post.find_all('p')
            text = []
            for paragraph in paragraphs:
                text.append(paragraph.text.strip())
            post_content = "".join(text)

            # Get post likes
            footer_element = post.find('footer').find('a')
            likes = footer_element.text
            # If there's no likes this text should be just "Like"
            if any(char.isdigit() for char in likes):
                num_likes = likes.split(' ')[0]
            else:
                num_likes = 0

            # Get number of comments
            footer = post.find('footer').find_all('a')
            comments = footer[3].text
            # If there's no comments this text should be just "Comment"
            if any(char.isdigit() for char in comments):
                num_comments = comments.split(' ')[0]
            else:
                num_comments = 0

            # Get comments for a post
            comments_list = []
            comment_link = 'https://mbasic.facebook.com/' + footer[3].get('href')
            get_comments(browser, comment_link, comments_list)
            posts_list.append({
                'content': post_content,
                'num_likes': num_likes,
                'num_comments': num_comments,
                'comments': comments_list
            })
            post_count = post_count + 1
        print(next_page_link)
        if next_page_link != None:
            next_url = 'https://mbasic.facebook.com/' + next_page_link
            get_posts(next_url, num_posts, browser, posts_list, post_count)
        return


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


def get_comments(browser, comments_url, comments_list) -> []:
    sleep(2)
    browser.get(comments_url)
    comment_page_soup = BeautifulSoup(browser.page_source, 'html.parser')
    comments_in_the_current_page = comment_page_soup.find('div', id='m_story_permalink_view').contents[1].contents[0].contents[4].contents
    # last div contains the link to next comment page, /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]
    print(len(comments_in_the_current_page))
    for index, comment in enumerate(comments_in_the_current_page):
        if index != len(comments_in_the_current_page) - 1 and index != 0:
            author = comment.find('h3').text
            comment_body = comment.find('div').text.replace(author, '')
            likes_img = comment.find('h3').find_next_siblings('div')[2].find('img')
            if likes_img:
                likes_num = likes_img.findParent('a').text
            else:
                likes_num = '0'
            comments_list.append(
                {'author': author, 'body': comment_body, 'likes_num': likes_num}
            )
    # go to next comment page and continue scraping
    if len(comments_in_the_current_page) > 0:
        if 'View more comments…' in comments_in_the_current_page[-1].text:
            next_comment_page = 'https://mbasic.facebook.com/' + comments_in_the_current_page[-1].find('a').get('href')
            get_comments(browser, next_comment_page, comments_list)

    return


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