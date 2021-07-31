import json
import re
import requests
from utils import *

# %205000users入り  %20表示被编码为空格
test = "https://www.pixiv.net/ajax/search/artworks/FGO%2010000users%E5%85%A5%E3%82%8A?word=FGO%2010000users%E5%85%A5%E3%82%8A&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh"
url = "https://www.pixiv.net/ajax/search/illustrations/FGO?word=FGO&order=date_d&mode=all&p=2&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh"
test2="https://www.pixiv.net/ajax/search/illustrations/FGO%205000users入り?word=FGO%205000users入り&order=date_d&mode=all&p=2&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh"

res = get_response(test).json()

for data in res['body']['illustManga']['data']:
    print(data['id'])
    img_detail_page = f"https://www.pixiv.net/artworks/{data['id']}"
    target_url =f"https://www.pixiv.net/ajax/illust/{data['id']}/pages?lang=zh"
    img_all = get_response(target_url).text
    img_original = re.findall('"original":"(.*?)"', img_all)
    img_data = get_image_data(img_detail_page)
    for img in img_original:
        print('收藏量:',img_data['bookmarkCount'])
        #  对于综合内容中不想下载排行榜的小说,跳过
        if len(img_original) > 1:
            break
        img = img.replace('\/', '/')
        print(f"{data['title']}  : {img}\n")
        check_image_resolution(img)
        download(img, fr"test/{data['title']}.jpg")
