#!/usr/bin/env python3

import argparse
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('user', metavar='USER', help=(
        'Specify the PlaysTV username.'))
args = parser.parse_args()

# there are obviously no PlaysTV's snapshot after the shutdown date,
# the Wayback Machine will automatically redirect us to the most recent one
shutdown_date = '20191215000000'
userpage = 'https://plays.tv/u/' + args.user
url = 'https://web.archive.org/web/' + shutdown_date + '/' + userpage

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# the number of user's videos is the first element of the array
userinfo = soup.findAll('span', {'class': 'section-value'})
videos_no = userinfo[0].text
print(args.user + ', ' + videos_no + ' videos')

# selenium web driver
driver = webdriver.Chrome()
driver.get(url)
time.sleep(1)
elem = driver.find_element_by_tag_name('body')

# weird PlaysTV counter problem
value = int(videos_no);
if ((args.user).lower() == "jakitv"):
    value = 92
elif ((args.user).lower() == "manfro"):
    value = 48

# get all the videos!
videos = []
while (len(videos) < value):
    body = driver.page_source
    soup = BeautifulSoup(body, 'html.parser')
    for video_list in soup.find_all('div', attrs={'class': 'content-1'}):
        video_list_descendants = video_list.descendants
        for video in video_list_descendants:
            if video.name == 'a' and video.get('class', '') == ['thumb-link']:
                href = video.get('href')
                if href not in videos:
                    videos.append(href)
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

# close the browser
driver.quit()

print(str(len(videos)) + ' video URLs found')

# remove first url part
for i, video in enumerate(videos):
    videos[i] = (video[video.find('video'):])

# remove all parameters from url
for i, video in enumerate(videos):
    videos[i] = video.split('?', 1)[0]
    
# reconstruct url
for i, video in enumerate(videos):
    videos[i] = 'https://web.archive.org/web/' + shutdown_date + '/https://plays.tv/' + video
    
#WIP
