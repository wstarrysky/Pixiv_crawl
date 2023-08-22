# coding = utf-8
"""
Author:starry sky
Email:wenbo_jiang@163.com

date:2021/12/4 15:15
describe:
"""
import asyncio
import json
import math
import re
import requests

from mode import ConfigItem
from utils import InitSet, Menu, bilibili_headers, proxies, download_aio


class BilibiliMode():
    def __init__(self):
        init = InitSet("bilibili")
        self.__items = [
            ConfigItem("searchCondition", "save_folder", init.bilibili_default_init["save_folder"]),  # 指定储存文件夹
            ConfigItem("searchCondition", "semaphore", init.bilibili_default_init["semaphore"]),  # 设置最大同时下载数,默认10
            ConfigItem("searchCondition", "single_page_num", init.bilibili_default_init["single_page_num"]),  # 单页显示数量
            ConfigItem("searchCondition", "start_page", init.bilibili_default_init["start_page"]),  # 下载开始的位置
            ConfigItem("searchCondition", "end_page", init.bilibili_default_init["end_page"]),  # 下载结束的位置
        ]
        for item in self.__items:
            setattr(self, item.option, item.process_value(item.default))  # 设置属性
        self.result = Menu(self, mode='bilibili')
        self.run()

    def run(self):
        img_pid_list = []
        cvnum = self._get_cvnum()
        total_page = math.ceil(cvnum / self.single_page_num)
        end_page = self.end_page if self.end_page is not None else total_page
        start_page = self.start_page if self.start_page is not None else 1
        for page in range(start_page, end_page + 1):
            get_cvid_params = {
                "mid": self.result.uid,  # up主UID
                "pn": page,  # 专栏页码
                "ps": self.single_page_num  # 一页显示的数量
            }
            get_cvid_url = "https://api.bilibili.com/x/space/article"  # 获取专栏id号
            res = requests.get(get_cvid_url, headers=bilibili_headers, params=get_cvid_params, proxies=proxies).json()
            for article in res.get('data').get('articles'):
                imglist = self._goto_cv(article.get('id'))
                if len(imglist) == 0:
                    print(f"cv{article.get('id')}没有图片/图片下方没有放置Pid")
                    continue
                print(f"cv{article.get('id')}共计{len(imglist)}张图片")
                print(imglist)
                for pid in [pid for pid in imglist]:
                    img_pid_list.append(pid)
        # print(f"准备下载专栏cv{}")
        print(f"共计{len(img_pid_list)}张图片")
        print(img_pid_list)
        # uid:18606111
        # img_pid_list = img_pid_list[::-1]
        id_download_url = f"https://www.pixiv.net/ajax/illust/"
        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(self.semaphore)  # 设置并发数
        tasks = []
        for pid in img_pid_list:
            # print(id_download_url + url)
            task = asyncio.ensure_future(download_aio(id_download_url+pid, semaphore, self.save_folder))
            # task.add_done_callback(callable)
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))

    def _goto_cv(self, cv_id):
        url = f"https://www.bilibili.com/read/cv{cv_id}"  # 获取cv专栏页面
        res = requests.get(url, headers=bilibili_headers, proxies=proxies).text
        imglist = re.findall('figcaption.*?(\d+).*?figca', res)
        imglist = [i for i in imglist if len(i)>=6]
        return imglist

    def _get_cvnum(self):
        """拿取cv专栏内容数量"""
        url = f"https://api.bilibili.com/x/space/navnum"
        params = {
            "mid": self.result.uid,
        }
        res = requests.get(url, headers=bilibili_headers, params=params, proxies=proxies).json()
        return res.get('data').get('article')
