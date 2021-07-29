import urllib.parse
import requests
import os
import re
from utils.config import *

'''
排行榜模式选择
1、 每日排行榜  格式:
https://www.pixiv.net/ranking.php?mode=daily&content=illust&date=20210727&p=2
2、 周排行榜   格式:
https://www.pixiv.net/ranking.php?mode=weekly&content=illust&date=20210727&p=2
3、每月排行榜   格式:
https://www.pixiv.net/ranking.php?mode=monthly&content=illust&date=20210726&p=2
'''


def get_response(html_url, stream=None, timeout=None):
    response = requests.get(url=html_url, headers=headers, proxies=proxies, stream=stream, timeout=timeout)
    return response


def download(url, filename):
    if not os.path.exists(os.path.split(filename)[0]):
        os.makedirs(os.path.split(filename)[0])
    r = get_response(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()


def check_image_resolution(img):
    pass
    # "width":2048,"height":1507,"pageCount":1,"bookmarkCount":400,"likeCount":233,"commentCount":1,"responseCount":0,"viewCount":1549,"


def get_image_data(img_detail_page):
    img_detal_text = get_response(img_detail_page).text
    keyAval = re.findall('"(width)":(\d*),"(height)":(\d*),"(pageCount)":(\d*),'
                         '"(bookmarkCount)":(\d*),"(likeCount)":(\d*),"(commentCount)":(\d*),"(responseCount)":(\d*),"(viewCount)":(\d*),"',
                         img_detal_text)
    data_dict = {}
    for i in range(0, len(keyAval[0]) - 1, 2):
        data_dict[keyAval[0][i]] = keyAval[0][i + 1]
    name = re.findall('illustTitle":"(.*?)"', img_detal_text)
    data_dict["name"] = str(name[0])
    return data_dict
