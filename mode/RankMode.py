import asyncio
import copy
import datetime
import re
from tqdm import tqdm

from mode.ConfigMode import ConfigItem
from utils import *
import time


class ToRankMode:
    # todo 排行榜下载模式在此文件
    __items = [
        ConfigItem("searchCondition", "DateTime", True),  # 是否对时间进行筛选
        ConfigItem("searchCondition", "page", False),  # 是否需要指定页数(默认第一页)
        ConfigItem("searchCondition", "save_folder", 'rank'),  # 指定储存文件夹
        ConfigItem("searchCondition", "rank_mode", '受男性欢迎'),  # 选择排行榜内容
        #  '''['今日','本周','本月','新人','受男性欢迎','受女性欢迎'](只有选择综合内容(all)才有(受男/女性欢迎模式)"'''
        ConfigItem("searchCondition", "rank_content", 'all'),  # 选择:['all','illustration','gif']
    ]

    def __init__(self):
        RANK_URL = "https://www.pixiv.net/ranking.php"
        for item in self.__items:
            setattr(self, item.option, item.process_value(item.default))
        self.result = Menu(self, mode='rank')

        self.date = "&date=" + (datetime.datetime.now() +
                                datetime.timedelta(days=-1)).strftime('%Y-%m-%d').replace('-', '')

        self.url = RANK_URL + self.result.rank_mode + self.result.rank_content

        # 启动函数
        if self.DateTime:
            for dt in self.result.dateList:
                self.temp_url = copy.deepcopy(self.url) + f"&date={dt}"
                self.run()
        else:
            self.url = self.url + self.result.dateList
            self.run()

    def run(self):
        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(10)  # 设置并发数
        tasks = []
        for page in self.result.pageList:
            url = self.url + page + "&format=json" if not self.DateTime else self.temp_url + page + "&format=json"
            print(url)
            page_content = get_response(url).json()
            img_original_json_url_list = []
            for img in tqdm(page_content['contents']):
                img_original_json_url = f"https://www.pixiv.net/ajax/illust/{img['illust_id']}"
                img_original_json_url_list.append(img_original_json_url)
            date = eval(re.findall('\d{8}', url)[0])

            for i, url in enumerate(img_original_json_url_list):
                task = asyncio.ensure_future(download_aio(url, semaphore, f"{self.save_folder}/{date}"))
                tasks.append(task)
            loop.run_until_complete(asyncio.wait(tasks))

    # def filter(self, img_data):
    #     """
    #     功能:如果满足条件则选择下载,否则跳过
    #     :param img_data: dict of image message
    #     :return: booling
    #     """
    #     if self.like_count != None:
    #         if not isinstance(self.like_count, int):
    #             print("like_count输入类型错误")
    #             exit()
    #         else:
    #             if int(img_data["likeCount"]) < self.like_count:
    #                 print(f"{img_data['name']}喜欢数为{img_data['likeCount']},小于设定值,跳过该图片")
    #                 return False
    #     if self.resolution != None:
    #         if not isinstance(self.resolution, str):
    #             print("like_count输入类型错误")
    #             exit()
    #         else:
    #             stand = {'1080': 1920 * 1080, '2k': 2560 * 1440, '4k': 3840 * 2160}
    #             if int(img_data['width']) * int(img_data['height']) < stand[self.resolution]:
    #                 print(f"{img_data['name']}\t分辨率为{int(img_data['width'])}X{int(img_data['height'])},小于设定值,跳过该图片")
    #                 return False
    #     return True
