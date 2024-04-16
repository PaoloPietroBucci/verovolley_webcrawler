from postget.posts import Posts
from postget.exceptions.exceptions import *

email = ''
username = ''
password = ''
# this is for snap chromium browser, you can change it to your own path
chromedriver = '/snap/bin/chromium.chromedriver'


def main():
    twitter_getter = Posts(username=username, password=password, email_address=email, query='',
                           num_scrolls=2, mode=1, wait_scroll_base=4, wait_scroll_epsilon=2, chromedriver=chromedriver)
    try:
        twitter_getter.login()
    except ElementNotLoaded as e:
        raise e

    print("Setting query in the object")
    twitter_getter.set_query('verovolley')

    print("Start Search, this will input the query and perform the scroll with the selected mode")
    try:
        twitter_getter.search()
    except ElementNotLoaded as e:
        raise e
    except NoTweetsReturned as e:
        print(e)

    print("Printing returned results and going home")
    twitter_getter.print_results()
    twitter_getter.go_home()
    print("Clearing Results")
    twitter_getter.clear_tweets()
    print("quitting browser")
    twitter_getter.quit_browser()


if __name__ == '__main__':
    main()
