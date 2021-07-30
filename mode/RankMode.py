import copy
import datetime
import re

from utils import *
import time


class ToRankMode:
    # todo 排行榜下载模式在此文件
    def __init__(self, rm, rc, d, p, sp='img', lc=None, res=None):
        if d:
            start_day = input("输入开始日期(年-月-日)")
            end_day = input("输入截止日期(年-月-日)")
            date_mode = input("输入日期计算方式(day、weekly、monthly)")
            self.date_list = self.get_datelist(start_day, end_day, mode=date_mode)
        # 筛选类变量
        self.like_count = lc
        self.resolution = res
        # 初始设置类变量
        self.save_path = sp
        self.page = p
        self.d = d
        self.date = "&date=" + (datetime.datetime.now() +
                                datetime.timedelta(days=-1)).strftime('%Y-%m-%d').replace('-', '')
        self.url = rank_url + \
                   rank_mode[rm] + \
                   rank_content[rc]

        # 启动函数
        if d:
            for dt in self.date_list:
                self.temp_url = copy.deepcopy(self.url) + f"&date={dt}"
                self.run()
        else:
            self.url = self.url + self.date
            self.run()

    def run(self):
        start_page = 1 if self.page == None else self.page[0]
        end_page = 2 if self.page == None else self.page[1] + 1
        for i in range(start_page, end_page):
            url = self.url + f"&p={i}" if not self.d else self.temp_url + f"&p={i}"
            print(url)
            date = eval(re.findall('\d{8}', url)[0])
            response = get_response(url, off=True).text
            reslut = re.findall('<section id.*?/section>', response)  # 图片概览页
            for test in reslut:
                message = re.findall('data-rank="(\d*)".*data-title="(.*?)".*data-id="(.*?)".*(/artworks/\d*?)"', test)
                print(f"排名{message[0][0]}")
                img_detail_page = f"https://www.pixiv.net/artworks/{message[0][2]}"  # 可以在详情页查看作品的信息
                target_html = f"https://www.pixiv.net/ajax/illust/{message[0][2]}/pages?lang=zh"  # 对于详情页有N张图片的情况可以展开
                img_all = get_response(target_html).text  # 图片详情页
                img_original = re.findall('"original":"(.*?)"', img_all)
                img_data = get_image_data(img_detail_page)
                if not self.filter(img_data):
                    continue
                count = 0
                for img in img_original:
                    #  对于综合内容中不想下载排行榜的小说,跳过
                    if len(img_original) > 1:
                        break
                    count += 1
                    img = img.replace('\/', '/')
                    print(f"{img_data['name']}  : {img}")
                    check_image_resolution(img)
                    download(img, fr"{self.save_path}/{date}/{message[0][0]}_{message[0][1]}_{count}.jpg")
                    # time.sleep(2)
                print('\n')

    def filter(self, img_data):
        """
        功能:如果满足条件则选择下载,否则跳过
        :param img_data: dict of image message
        :return: booling
        """
        if self.like_count != None:
            if not isinstance(self.like_count, int):
                print("like_count输入类型错误")
                exit()
            else:
                if int(img_data["likeCount"]) < self.like_count:
                    print(f"{img_data['name']}喜欢数为{img_data['likeCount']},小于设定值,跳过该图片")
                    return False
        if self.resolution != None:
            if not isinstance(self.resolution, str):
                print("like_count输入类型错误")
                exit()
            else:
                stand = {'1080': 1920 * 1080, '2k': 2560 * 1440, '4k': 3840 * 2160}
                if int(img_data['width']) * int(img_data['height']) < stand[self.resolution]:
                    print(f"{img_data['name']}\t分辨率为{int(img_data['width'])}X{int(img_data['height'])},小于设定值,跳过该图片")
                    return False
        return True

    def get_datelist(self, start_day, end_day, mode="day"):
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
