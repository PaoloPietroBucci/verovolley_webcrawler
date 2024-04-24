# Sections
- [Purpose](#purpose)
- [Setup](#setup)
    - [Chromedriver](#chromedriver)
    - [Virtual Environment](#virtual-environment)
- [Usage](#usage)
  - [Facebook](#facebook)
  - [Instagram](#instagram)
  - [LinkedIn](#linkedin)
  - [X](#x)
    - [CLI](#cli---examples)
    - [Operating mode](#operating-mode)
    - [Command Line](#command-line)
    - [Main parameters](#main-parameters-in-the-initialization)
  - [Web pages](#web-pages)


# Purpose
**This package is intended EXCLUSIVELY for academic research and demonstrative purposes. The authors have no responsibility for the use the tool will be used in and the consequences of it. Keep in mind that running this code is forbidden, is just a demonstration of how scraping works. If you decide to run it anyway, you will assume all the responsibilities for the consequences it will have.**

# Setup
To use the crawlers for [Facebook](#facebook), [LinkedIn](#linkedin) and [X](#x) the installation of the Chrome browser and ChromeDriver is required. Chromedriver is a standalone server that implements the [W3C WebDriver standard](https://w3c.github.io/webdriver/), which is an open source tool for automated testing of webapps.

## Installing Chrome
Navigate to [Google Chrome’s](https://www.google.com/chrome/) official website and download the appropriate version for your operating system.

If you use Ubuntu, you can instead install Chrome through the snap store. If done with this method, chromedriver should be installed automatically. You may check it by [verifying](#2-verify-chromedriver) if present in your machine and if present you can skip the chromedriver installation described in the next step.

## Installing Chromedriver
Notice that this is **required** for most of the presented packages to work. 
### 1. Determine your Chrome version
Open Google Chrome, click on the **three vertical dots** on the top right **-> Help -> About Google Chrome**. Note down the version number.
### 2. Download the appropriate ChromeDriver
Visit the [ChromeDriver](https://chromedriver.chromium.org/downloads) download page and download the version that matches your Chrome version.
### 3. Extract and move ChromeDriver:
```
unzip chromedriver_win32.zip          # For Windows
tar -xvf chromedriver_mac64.zip       # For Mac
tar -xvf chromedriver_linux64.tar.gz  # For Linux
```
Move the `chromedriver` to `/usr/bin/` or any location in your system’s PATH:
```
sudo mv chromedriver /usr/bin/
```
*Tested on [chromium](https://googlechromelabs.github.io/chrome-for-testing/) and [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) v.123.0.6312.122*

## Virtual Environment
Creation of a new virtual environment is **highly recommended**, every time you a crawler for a different social. 

In the home folder of a linux system:
```
python3 -m venv ./venv
```
Acrivate it:
```
source venv/bin/activate
```
Navigate to the folder of the social you want to work with and install the requirements of the package:
```
pip install -r requirements.txt
```


## Verifying Installation
### 1. Verify Google Chrome:
Run `google-chrome` from the terminal  or find Google Chrome in your applications and launch it.
### 2. Verify ChromeDriver:
```
chromedriver --version
```
This should match the Google Chrome version you noted earlier.
### 3. Verify Selenium:
```
pip show selenium
```
This will display Selenium package details, confirming its installation in your virtual environment.

---
# Usage
Since every social was created with a different architecture in mind, the methods to extract data may differ for one another. Nonetheless, for an easier use, we tried to maintain the same formatting in the parser throughout the different platforms, changes may be encountered in the arguments to pass. 

Once the command is sent, the program will begin its execution accessing the social with credentials (if needed) and will start scraping the specified info, once its done the program will create a .json file that can be used in a MongoDB environment, ready to be analyzed. Below you can find the CLI parameters that can be passed per social scraper.  

___
## Facebook
... *in development*
 
___
## Instagram
### To Implement
- Post filtering by date

### CLI - examples
An example of command is (in the following a detailed explanation is provided):
```
python3 main.py --username '<your_username>' --password '<your_password>' --query '<query_to_be_performed>' 
```

### Command Line
You can use this package from command line, `postget` will:
1. log in a new session or a previously created one
2. search for the query according to the operating mode
3. save found information in a .json file that can be used in a MongoDB environment according to the operating mode
4. close the driver

Notice that this means that a second call will imply a new login phase.

### Main parameters in the initialization
Parameter | type                                                                    | Description
--- |-------------------------------------------------------------------------| ---
`username` | (`str`):                                                                |Username that will be used to access the Instagram account
`password` | (`str`):                                                                |Password of the Username that will be used access the Instagram account
`query` | (`str`):                                                                |Profile to be searched on Instagram
`reels` | (`bool` if imported, just type `--reels` if called from command line):  |Call with this if you want get list of reels as the only media
`tag` | (`bool` if imported, just type `--tag` if called from command line):    |Call with this if you want get list of only the posts the user was tagged in
`hashtag` | (`str`):                                                                |Hashtag to be searched on Instagram. With a list of related posts under the hashtag
`recent_hash` | (`int`):                                                                |Return the selected amount of most recent posts by hashtag. If set to `-1` (default value) this parameter will not be considered. 
`top_hash` | (`int`):                                                                |Return the selected amount of top posts by hashtag. If set to `-1` (default value) this parameter will not be considered. 
`num_posts` | (`int`):                                                                |Number of posts to scrape starting from the most recent one. Set to `3` (default value).
`comments` | (`int`):                                                                |Number of comments to scrape from each post. Set to `0` (default value) means all the comments of the post will be saved.
`likers` | (`bool` if imported, just type `--likers` if called from command line): |Call with this if you also want get list of users who liked the post (due to Instagram limitations, this may not return a complete list)
`bio` | (`bool` if imported, just type `--bio` if called from command line):    |Call with this if you also want get the bio of the user you are searching for
`followers` | (`int`):                                                                |Call with this if you also want get a list of the amount of users who followers the user. If set to `-1` (default value) this parameter will not be considered. 
`following` | (`int`):                                                                |Call with this if you also want get a list of the amount of users who the user follows. If set to `-1` (default value) this parameter will not be considered. 
`story` | (`int`):                                                                |Call with this if you also want get a list of the amount of stories published by the user. If set to `-1` (default value) this parameter will not be considered. 

___
## Linkedin
... *in development*

___
## X
*The package used for the X social media platform builds upon [postget](https://github.com/alessandriniluca/postget) created by [alessandriniluca](https://github.com/alessandriniluca). We extend our gratitude to the original authors for their foundational work.*   

### CLI - examples
An example of command is (in the following a detailed explanation is provided):
```
python3 main.py --username '<your_username>' --password '<your_password>' --query '<query_to_be_performed>' --email_address '<mail_of_the_account>' --num_scrolls 10  --wait_scroll_base 3 --wait_scroll_epsilon 1  --mode 1
```

### Operating mode

`postget` searches for images and tweet in two different ways:
- **Mode `0`**, or *simple search*: it just grep all links of images and videos detected when scrolling
- **Mode `1`**, or *complete search*: it greps also all information of tweet, such as id of the discussion and author. Notice that if you want to perform the search within two tweets' ids, it is necessary to operate in this mode.

Why keeping both? Because in mode `1` many things can go wrong, it is sufficient that one div search fails, that the entire search crashes. 

### Command Line
You can use this package from command line, `postget` will:
1. log in
2.  search for the query according to the operating mode
3. perform scrolls
4. print the images and video previews links or the tweets information according to the operating mode
5. save the found information in a .json file that can be used in a MongoDB environment
6. close the driver

Notice that this means that a second call will imply a new login phase.

### Main parameters in the initialization
Parameter | type | Description
--- | --- | ---
`username` |(`str`): |Username that will be used to access the Twitter account
`password` |(`str`): |Password of the Username that will be used access the Twitter account
`query` |(`str`): |Query to be searched on Twitter
`wait_scroll_base` |(`int`): |base time to wait between one scroll and the subsequent (expressed in number of seconds, default 15)
`wait_scroll_epsilon` |(`float`): |random time to be added to the base time to wait between one scroll and the subsequent, in order to avoid being detected as a bot (expressed in number of seconds, default 5)
`num_scrolls` |(`int`): |number of scrolls to be performed, default 10
`since_id` |(`int`): |id from which tweets will be saved (tweets with an id `<` with respect than this value will be discarded). If set to `-1` (default value), this parameter will not be considered. Notice that this will be considered only if also `max_id` will be set, and will work only for search mode equal to `1`
`max_id` |(`int`): |id until tweets will be saved (tweets with an id `>` with respect to this value, will be discarded). Notice that this will be considered only if also `max_id` will be set, and will work only for search mode equal to `1`
`mode` |(`int`): |selects the operating mode, the default is `0`.
`since` |(`str`): |String of the date (excluded) from which the tweets will be returned. Format: `YYYY-MM-DD`, UTC time. Temporarily supported only for mode `1`. If you set also since_time, or until_time, this will be ignored. Wrong formats will be ignored
`until` |(`str`): |String of the date (included) until which the tweets will be returned. Format: `YYYY-MM-DD`, UTC time. Temporarily supported only for mode `1`. If you set also since_time, or until_time, this will be ignored. Wrong formats will be ignored
`since_time` |(`str`): |String of the time from which the tweets will be returned. Format: timestamp in SECONDS, UTC time. Temporarily supported only for mode `1`
`until_time` |(`str`): |String of the time until which the tweets will be returned. Format: timestamp in SECONDS, UTC time. Temporarily supported only for mode `1`
`headless` |(`bool` if imported, just type `--headles` if called from command line): |If specified, runs the browser in headless mode. Unfortunately something changed from the first version of postget, and this is no more working. A section in the roadmap has been added for this.
`chromedriver` |(`str`): |custom path to the chromedriver. if not specified, the code will try to find automatically the path of `chromedriver`
`email_address` |(`str`): |email of the account, required since sometimes could be asked to insert it to verify the account
`root` |(`bool` if imported, just type `--root` if called from command line): |If specified, adds the option `--no-sandbox` to the chrome options, needed to be runned in root mode. Please notice that running in root mode is **not** safe for security reasons.

A couple of words on advenced filters:

- `since_id` and `max_id`: if one of them is not set, or set to the default value, also the other correctly set will be ignored. If correctly set, tweets with the id within `[since_id, max_id]` will be saved (extremes included).
- Precedences among `since_id`, `max_id`, `since`, `until`, `since_time`, `until_time`:
    - The definition of even just one parameter among `since`, or `until` causes the invalidation of `since_id` and `max_id` (they simply will not be considered).
    - The definition of even just one parameter among `since_time` or `until_time` causes the invalidation of `since` and `until` (they simply will not be considered). The same reasoning will be applied to `since_id` and `max_id` when one among `since_time` or `until_time` is defined.
___

## Web pages
...
