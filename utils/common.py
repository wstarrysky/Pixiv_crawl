import datetime
import urllib.parse

import aiohttp
import requests
import os
import re

from colorama import Fore, Back, Style

from utils.config import *

'''
异步获取
'''


# *****************************************标签模式异步下载******************************************************
async def get_response_aio(url):
    pattern = re.compile(r'\d+')
    pid = re.findall(pattern, url)[0]
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url=url, headers=headers, proxy=proxy) as title:
            img_data = await title.json()
            # print(type(img_data))
            # img_title = img_data['body']['title']
            # img_original_url = img_data['body']['urls']['original']
            if isinstance(img_data,dict):
                if isinstance(img_data['body'],list):
                    print('\033[31m'+f'{url} 该图片已经被删除  pid:{pid}'+'\033[0m')
                    return None,None
                img_title = img_data['body']['title']
                img_original_url = img_data['body']['urls']['original']
            else:
                print(url)
                print(img_data)
                return None,None
        return img_title, img_original_url


async def download_aio(download_url, semaphore, save_folder="./"):
    '''
    通过每一张图片的详情页url则可以进行下载 eg:'https://www.pixiv.net/ajax/illust/91601644'(每一张图片不同的就只是id问题而已)
    对这个url发送请求得到json文件,获取图片的标题title、原图片的链接original

    再对原图片的链接发送请求进行流式下载
    '''
    pid = re.findall(r'\d+', download_url)[0]
    show_url = f"https://www.pixiv.net/artworks/{pid}"
    img_title, img_original_url= await get_response_aio(download_url)
    if img_title is None:
        return
    img_name = re.sub('[\\\\/:*?\"<>|]', '', img_title)  # 替换非法字符
    ext = img_original_url.split('.')[-1]
    img_name = img_name + '.' + ext
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    else:
        file_name_list = os.listdir(save_folder)
        if img_name in file_name_list:
            print('\033[34m'+f"{img_name}"+'\033[0m'+"已经存在 ")
            return
    file_name = os.path.join(save_folder, img_name)
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as session:
                img = await session.get(img_original_url, headers=headers, proxy=proxy)
                print(f"\033[32m正在下载{img_name}  原图url:{img_original_url}  p站url:{show_url}\033[0m")
                img.raise_for_status()
                with open(file_name, 'wb') as f:
                    while True:
                        chunk = await img.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        f.flush()
            print('下载成功!' + file_name)
        except:

            with open("download_error.txt", "a+", encoding='utf-8') as f:
                f.write(f"{file_name}\t : {url}\n\n")
            file_path = f"{save_folder}/{file_name}"
            os.remove(file_path)
            print(f"\033[1;33m下载失败!{file_name}  {url}\033[0m")


'''
同步获取
'''


def get_response(html_url, stream=None, timeout=None, off=False):
    if off == True:
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
    response = requests.get(url=html_url, headers=headers, proxies=proxies, stream=stream, timeout=timeout)
    return response


def download(url, filename):
    filename = re.sub('[\\\\:*?\"<>|]', '', filename)  # 替换非法字符

    if not os.path.exists(filename):
        if not os.path.exists(os.path.split(filename)[0]):
            os.makedirs(os.path.split(filename)[0])
        r = get_response(url, stream=True, timeout=60, off=True)
        r.raise_for_status()
        with open(f"{filename}", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.seek(0, 2)
                    f.write(chunk)
                    f.flush()
    else:
        print(filename, '已经存在')


def check_image_resolution(img):
    pass
    # "width":2048,"height":1507,"pageCount":1,"bookmarkCount":400,"likeCount":233,"commentCount":1,"responseCount":0,"viewCount":1549,"


def get_datelist(start_day, end_day, mode="day"):
    num = {'day': 1,
           'weekly': 7,
           'monthly': 30
           }
    datestart = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_day, '%Y-%m-%d')
    date_list = []
    while datestart <= dateend:
        date_list.append(dateend.strftime('%Y-%m-%d').replace('-', ''))
        dateend -= datetime.timedelta(days=num[mode])
    return date_list


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


def get_imgId(page_json):
    page_illust = page_json['body']['illust']
    page_data = page_illust['data']
    return page_data


def display_head(mode):
    PADDING = 70
    print("┌" + "".ljust(PADDING - 1, "─") + "┐")
    print(
        "│ " + Fore.YELLOW + Back.BLACK + Style.BRIGHT + f"Pixiv_Crawl version {1}".ljust(
            PADDING - 3, " ") + Style.RESET_ALL + " │")
    print("│ " + Fore.CYAN + Back.BLACK + Style.BRIGHT + '------starry sky------'.ljust(PADDING - 3,
                                                                                        " ") + Style.RESET_ALL + " │")
    # print(
    #     "│ " + Fore.YELLOW + Back.BLACK + Style.BRIGHT + f"For learning and communication only".ljust(
    #         PADDING - 3, " ") + Style.RESET_ALL + " │")
    # print(
    #     "│ " + Fore.YELLOW + Back.BLACK + Style.BRIGHT + f"Please support genuine edition outside of study".ljust(
    #         PADDING-3, " ") + Style.RESET_ALL + " │")
    print(
        "│ " + Fore.LIGHTGREEN_EX + Back.BLACK + Style.BRIGHT + f"当前模式{Fore.CYAN}{Style.BRIGHT}   {mode}".ljust(
            PADDING+1, " ") + Style.RESET_ALL + " │")
    print("└" + "".ljust(PADDING - 1, "─") + "┘")
