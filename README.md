# VVolley_webscraper
Descrizione: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 

## Sections
- [Intent](#intent)
- [Setup](#setup)
    - [Chromedriver](#chromedriver)
    - [Virtual Environment](#virtual-environment)
- [Usage](#usage)
  - [Facebook](#facebook)
  - [Instagram](#instagram)
  - [X ](#x)
  - [Web pages](#web-pages)


## Intent
<u>**This package is intended EXCLUSIVELY for academic research and demonstrative purposes. The authors have no responsibility for the use the tool will be used in and the consequences of it. Keep in mind that running this code is forbidden, is just a demonstration of how scraping works. If you decide to run it anyway, you will assume all the responsibilities for the consequences it will have.**</u>

## Setup
### Chromedriver
Notice that this is **required** for this package to work. To install it, it is enough to install chromium and the chromedriver.

The path of `chromedriver` is found automatically. If your operating system for whatever reason gives it another name, pass it through the parameter `chromedriver`.

Tested on [chromium](https://googlechromelabs.github.io/chrome-for-testing/) and [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) v.123.0.6312.105



### Virtual Environment
Creation of a virtual environment is **highly recommended**. In the home folder of a linux system:
```
python3 -m venv ./venv
```
Acrivate it:
```
source venv/bin/activate
```
Install the requirements of the package:
```
pip install -r requirements.txt
```
Install the package. It is **highly suggested** to install it in the editor mode, to allow changes without need of re-install it every time. Enter the path of the folder which contains this file, and type from the terminal:
```
pip install -e .
```
To test the installation, try to type (inside the virtual environment):
```
postget --help
```
If the response is correct and show the output of a help command, then it is working.


## Usage
...

### Facebook
...

### Instagram
...

### X
The package used for the X social media platform builds upon [postget](https://github.com/alessandriniluca/postget) created by [alessandriniluca](https://github.com/alessandriniluca). We extend our gratitude to the original authors for their foundational work.   

### Web pages
...
