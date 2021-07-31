import datetime

from utils.config import *
from utils.common import get_datelist
import traceback


class Menu:
    result = []

    def __init__(self, modeset, mode=None):
        if mode == 'tags':
            self.tag = input("输入标签")
            self.bookmarkCount = self.__get_bookmark_count() if modeset.bookmarkCount else ''
            self.KeyWord = '?word=' + self.tag + self.bookmarkCount
            self.order = '&order=date_d' if modeset.order else '&order=date'
            self.sectionTag = "&s_mode=s_tag" if modeset.sectionTag else "&s_mode=s_tag_full"
            self.illType = "&type=illust" if not modeset.illType else "&type=illust_and_ugoira"
            self.resolution = self.__get_resolution() if modeset.resolution else ''
            self.ratio = self.__get_ratio() if modeset.ratio else ''
            self.pageList = self.__get_page_list() if modeset.page else ['&p=1']

            # self.dateList = self.__get_data_list() if modeset.DataTime else [
            #     datetime.datetime.today().strftime('%Y-%m-%d').replace('-', '')]

        elif mode == 'rank':
            # todo 菜单排行榜模式待完成
            self.pageList = self.__get_page_list() if modeset.page else ['&p=1']
            self.dateList = self.__get_data_list() if modeset.DateTime else [
                "&date=" + (datetime.datetime.now() +
                            datetime.timedelta(days=-1)).strftime('%Y-%m-%d').replace('-', '')]
            self.rank_mode = rank_mode[modeset.rank_mode]
            self.rank_content = rank_content[modeset.rank_content]
            pass
        elif mode == 'id':
            # todo 菜单id下载模式待完成
            pass
        else:
            raise Exception('未输入mode参数')

    def __get_data_list(self):
        while True:
            start_day = input("输入开始日期(年-月-日)")
            if len(start_day) != 10:
                print('输入错误,重新输入')
            else:
                break
        while True:
            end_day = input("输入截止日期(年-月-日)")
            if len(end_day) != 10:
                print('输入错误,重新输入')
            else:
                datestart = datetime.datetime.strptime(start_day, '%Y-%m-%d')
                dateend = datetime.datetime.strptime(end_day, '%Y-%m-%d')
                if datestart >= dateend:
                    print('输入错误,重新输入')
                else:
                    break
        while True:
            date_mode = input("输入日期计算方式(day、weekly、monthly)")
            if date_mode not in ['day', 'weekly', 'monthly']:
                print('输入错误,重新输入')
            else:
                break
        datelist = get_datelist(start_day, end_day, mode=date_mode)
        return datelist

    def __get_bookmark_count(self):
        num = int(input("输入最小收藏数量(整数)"))
        bookmarkCount = f"%20{num}users入り"
        return bookmarkCount

    def __get_resolution(self):
        print('选择分辨率要求:\n1.3000^2以上\n2.1000^2~3000^2\n3.1000^2以下(输入1 2 3)')
        d = {
            "1": "&wlt=3000&hlt=3000",
            "2": "&wlt=1000&wgt=2999&hlt=1000&hgt=2999",
            "3": "&wgt=999&hgt=999"
        }
        f = 0
        while 0 < f <= 3:
            f = eval(input('输入'))
            if not isinstance(f, int):
                print('输入类型错误,重新输入')
        resolution = d[f'{f}']
        return resolution

    def __get_ratio(self):
        print('选择方向:\n1.横图\n2.纵图\n3.正方形')
        d = {
            "1": "&ratio=0.5",
            "2": "&ratio=-0.5",
            "3": "&ratio=0"
        }
        f = 0
        while 0 < f <= 3:
            f = eval(input('输入'))
            if not isinstance(f, int):
                print('输入类型错误,重新输入')
        ratio = d[f'{f}']
        return ratio

    def __get_page_list(self):
        while True:
            start_page = eval(input('输入开始的页码(整数)'))
            if isinstance(start_page, int) and start_page > 0:
                break
            else:
                print('输入无效,重新输入')
        while True:
            end_page = eval(input('输入截止的页码(整数)'))
            if isinstance(end_page, int) and end_page > start_page:
                break
            else:
                print('输入无效,重新输入')
        pageList = [f"&p={i}" for i in range(start_page, end_page + 1)]
        return pageList
