import asyncio
import copy
import datetime
import os
import re
from tqdm import tqdm
from utils import Menu, InitSet, CheckInputFormat
from mode.ConfigMode import ConfigItem
from utils.common import get_response, get_response_aio, get_imgId, download_aio
from utils.config import *


class IDMode:
    # todo 标签下载模式在此文件

    def __init__(self):
        self.check = CheckInputFormat()  # 检查输入是否正确

        init = InitSet("id")
        self.__items = [
            ConfigItem("searchCondition", "idlist", init.id_default_init['idlist']),  # 单次输入id下载还是通过 id list进行下载
            ConfigItem("searchCondition", "read_folder", init.id_default_init['read_folder']),  # 读取文件的路径
            ConfigItem("searchCondition", "save_folder", init.id_default_init["save_folder"]),  # 指定储存文件夹
            ConfigItem("searchCondition", "semaphore", init.id_default_init["semaphore"]),  # 设置最大同时下载数,默认10
        ]
        self._base_url = f"https://www.pixiv.net/ajax/illust/"

        for item in self.__items:
            setattr(self, item.option, item.process_value(item.default))
        self.result = Menu(self, mode='id')

        self.run()

    def run(self):
        if self.idlist:
            # 打开txt文件进行读取
            with open('./id_download.txt', 'r', encoding='utf-8') as download_file:
                download_list = re.findall('\d+', download_file.read())
                img_original_json_url_list = []
                for id in tqdm(download_list):
                    try:
                        self.temp_url = self._base_url + id
                        img_original_json_url_list.append(self.temp_url)
                    except:
                        continue
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(self.semaphore)  # 设置并发数
                tasks = []
                for i, url in enumerate(img_original_json_url_list):
                    task = asyncio.ensure_future(download_aio(url, semaphore, self.save_folder))
                    # task.add_done_callback(callable)
                    tasks.append(task)
                loop.run_until_complete(asyncio.wait(tasks))
        else:
            while True:
                id = input('输入要下载的图片的id')
                id = re.findall('\d.{7,9}', id)
                # url = self._base_url + str(id)
                loop = asyncio.get_event_loop()
                semaphore = asyncio.Semaphore(self.semaphore)  # 设置并发数
                tasks = []
                for i, url in enumerate([*id]):
                    task = asyncio.ensure_future(download_aio(self._base_url+url, semaphore, self.save_folder))
                    # task.add_done_callback(callable)
                    tasks.append(task)
                loop.run_until_complete(asyncio.wait(tasks))

                n = self.check.input('\n是否下载完毕?继续下载按Y,退出按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                     str_list=['Y', 'y', 'N', 'n'])
                if n in ['N', 'n']:
                    break
