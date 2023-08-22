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


# https://www.pixiv.net/ajax/search/illustrations/FGO%205000users入り?
# word=FGO%205000users入り&order=date_d&mode=all&p=2&s_mode=s_tag_full&type=illust_and_ugoira&lang=zh

# base_url + Tags + bookmarkCount + ? + word=keyword & order & mode=all & page &sectionTag & type=illust_and_ugoira
# &lang=zh  + &wlt=3000&hlt=3000  +

# https://www.pixiv.net/tags/Fate%2FGrandOrder/illustrations?p=3&date=20210723
# https://www.pixiv.net/tags/Fate%2FGrandOrder/illustrations?s_mode=s_tag  标签部分一致
# https://www.pixiv.net/tags/Fate%2FGrandOrder/illustrations?type=illust   标签完全一致
# &wlt=3000&hlt=3000 清晰度的筛选    &ratio=0.5  横图的筛选  &ratio=-0.5  纵图的筛选  &ratio=0 正方形图的筛选
# date_d 最新排序 date最旧排序
# type=illust  只选择插画  type=illust_and_ugoira 选择插画与动图
# https://www.pixiv.net/ajax/search/illustrations/FGO?word=FGO&order=date&mode=all&p=1&s_mode=s_tag_full&type=illust_and_ugoira&wlt=1000&wgt=2999&hlt=1000&hgt=2999&lang=zh


class TagsMode():

    # https://www.pixiv.net/ajax/search/illustrations/FGO?word=FGO&order=date_d&mode=all&p=1&s_mode=s_tag&type=illust_and_ugoira&lang=zh
    def __init__(self):
        self.check = CheckInputFormat()
        init = InitSet("tags")
        self.__items = [
            ConfigItem("searchCondition", "bookmarkCount", init.tags_default_init['bookmarkCount']),  # 是否启用收藏筛选模式
            ConfigItem("searchCondition", "order", init.tags_default_init['order']),  # 是否按照最新排序(否:最旧排序)
            ConfigItem("searchCondition", "page", init.tags_default_init['page']),  # 是否需要指定页数(默认第一页)
            ConfigItem("searchCondition", "sectionTag", init.tags_default_init['sectionTag']),  # 是否启用部分标签
            ConfigItem("searchCondition", "illType", init.tags_default_init['illType']),  # 是否需要选取动图
            ConfigItem("searchCondition", "resolution", init.tags_default_init['resolution']),  # 是否启用清晰度筛选
            ConfigItem("searchCondition", "ratio", init.tags_default_init['ratio']),  # 是否对横纵比进行筛选
            ConfigItem("searchCondition", "save_folder", init.tags_default_init['save_folder']),  # 指定储存文件夹
            ConfigItem("searchCondition", "semaphore", init.tags_default_init["semaphore"]),  # 设置最大同时下载数,默认10

            # ConfigItem("searchCondition", "DataTime", False),  # 是否对时间进行筛选
        ]
        self._base_url = "https://www.pixiv.net/ajax/search/illustrations/"
        for item in self.__items:
            setattr(self, item.option, item.process_value(item.default))

        self.result = Menu(self, mode='tags')
        self.target_url = self._get_target_url()
        self.run()



    # https://www.pixiv.net/ajax/search/illustrations/FGO%2010000users%E5%85%A5%E3%82%8A?word=FGO%2010000users%E5%85%A5%E3%82%8A&order=date_d&mode=all&p=1&s_mode=s_tag&type=illust_and_ugoira&lang=zh
    def run(self):
        chenk_content = get_response(self.target_url).json()
        while len(get_imgId(chenk_content)) == 0:
            print("标签内容为空,请重新输入内容")
            self.result.tag = input("输入标签:")
            self.result.bookmarkCount = f"%20{self.check.input('输入最小收藏数量(整数):', CHECK_MODE_INT_RANGE)}users入り"
            self.target_url = self._get_target_url()
            chenk_content = get_response(self.target_url).json()
        for t, page in enumerate(self.result.pageList):
            save_folder = os.path.join(os.path.join(self.save_folder, self.result.tag), f"第{t + 1}页")
            self.tempUrl = self.target_url + page
            print(self.tempUrl)
            page_json = get_response(self.tempUrl).json()
            img_original_json_url_list = []
            for img_data in tqdm(get_imgId(page_json)):
                try:
                    img_original_json_url = f"https://www.pixiv.net/ajax/illust/{img_data['id']}"
                    img_original_json_url_list.append(img_original_json_url)
                except:
                    continue
            loop = asyncio.get_event_loop()
            semaphore = asyncio.Semaphore(self.semaphore)  # 设置并发数
            tasks = []
            for i, url in enumerate(img_original_json_url_list):
                task = asyncio.ensure_future(download_aio(url, semaphore, save_folder))
                # task.add_done_callback(callable)
                tasks.append(task)
            loop.run_until_complete(asyncio.wait(tasks))

    def _get_target_url(self):
        return self._base_url + self.result.tag + self.result.bookmarkCount + self.result.KeyWord + \
               self.result.order + self.result.sectionTag + self.result.illType + \
               self.result.resolution + self.result.ratio

    def paser_tags_page(self):
        pass

    def get_datelist(self, start_day, end_day, mode):
        pass
