import datetime
import re

from colorama import Fore, Back, Style

from utils.config import *
from utils.common import get_datelist, display_head
import traceback




class CheckInputFormat:
    '''
    对输入的文本进行检查
    1. 检查输入格式是否是年月日格式   **** - ** - **
    2. 检查输入整数是否在指定范围    min_val max_val
    3. 检查输入内容是否在是指定的字符串 str_list
    '''

    def input(self, prin_content: str, check_mode: int, min_val=None, max_val=None, str_list=None):
        if check_mode == 0:
            #  检查日期格式
            while True:
                input_result = input(prin_content)
                input_result = re.sub('[^0-9-]', '', input_result)
                if len(input_result) != 10:
                    print('输入格式错误,重新输入')
                else:
                    return input_result

        elif check_mode == 1:
            #   检查输入整数范围
            while True:
                input_result = input(prin_content)
                input_result = re.sub('[ \t]', '', input_result)
                input_result.isdigit()
                if not input_result.isdigit():
                    print('输入类型错误,重新输入')
                    continue

                input_result = int(input_result)
                if min_val is not None and max_val is not None:
                    if not min_val <= input_result <= max_val:
                        print('输入范围错误,重新输入')
                        continue
                elif min_val is not None and max_val is None:
                    if not min_val <= input_result:
                        print('输入范围错误,重新输入')
                        continue
                elif min_val is None and max_val is not None:
                    if not input_result <= max_val:
                        print('输入范围错误,重新输入')
                        continue
                return input_result

        elif check_mode == 2:
            #   检查输入是否在指定的字符串列表
            while True:
                input_result = input(prin_content)
                if input_result not in str_list:
                    print('输入字符不在范围内,重新输入')
                    continue
                return input_result

        else:
            raise ValueError('模式选择错误')


class InitSet:

    def __init__(self, mode):
        self.rank_default_init = {"DateTime": False,
                                  "page": False,
                                  "save_folder": 'rank',
                                  "rank_content": 'all',
                                  "rank_mode": '受男性欢迎',
                                  "semaphore": 10,
                                  }

        self.tags_default_init = {"bookmarkCount": True,
                                  "order": True,
                                  "page": False,
                                  "sectionTag": True,
                                  "illType": False,
                                  "resolution": False,
                                  "ratio": False,
                                  "save_folder": 'tags',
                                  "semaphore": 10,
                                  }
        self.id_default_init = {"idlist": False,
                                "read_folder": 'id_download.txt',
                                "save_folder": 'id_download',
                                "semaphore": 10,
                                }
        self.check = CheckInputFormat()
        if mode == 'rank':
            self.init_rank_print()
        elif mode == 'tags':
            self.init_tags_print()
        elif mode == 'id':
            self.init_id_print()

    def init_rank_print(self):
        display_head("排行榜模式")

        print('1. 是否对时间进行筛选,默认关闭')
        print('2. 是否需要指定页数范围,默认第一页')
        print('3. 是否需要指定储存文件夹,默认文件夹为rank文件夹')
        print('4. 选择内容版块(["all","illustration","gif"]),默认为all')
        print("5. 选择筛选方式(['今日','本周','本月','新人','受男性欢迎','受女性欢迎']),"
              "只有选择综合内容(all)才有(受男/女性欢迎模式),默认为'受男性欢迎'")
        print('6. 是否需要修改最大同时下载数量,默认为10')

        juge = self.check.input('\n使用默认方式请按Y,需要更改请按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                str_list=['Y', 'y', 'N', 'n'])
        if juge in ['Y', 'y']:
            return self.rank_default_init
        elif juge in ['N', 'n']:
            while True:
                re = self.check.input('选择需要更改的内容', check_mode=CHECK_MODE_INT_RANGE, min_val=1, max_val=6)
                if re == 1:
                    self.rank_default_init['DateTime'] = not self.rank_default_init['DateTime']
                    print('时间选择模式已开启') if self.rank_default_init['DateTime'] else print('时间选择模式已关闭')
                elif re == 2:
                    self.rank_default_init['page'] = not self.rank_default_init['page']
                    print('指定页码范围模式已开启') if self.rank_default_init['page'] else print('指定页码范围模式已关闭')
                elif re == 3:
                    self.rank_default_init['save_folder'] = input('输入储存文件夹')
                elif re == 4:
                    self.rank_default_init['rank_content'] = self.check.input('选择内容版块(["all","illustration","gif"])',
                                                                              check_mode=CHECK_MODE_STR_LIST,
                                                                              str_list=["all", "illustration", "gif"])
                elif re == 5:
                    self.rank_default_init['rank_content'] = self.check.input(
                        "选择筛选方式(['今日','本周','本月','新人','受男性欢迎','受女性欢迎']",
                        check_mode=CHECK_MODE_STR_LIST,
                        str_list=['今日', '本周', '本月', '新人', '受男性欢迎', '受女性欢迎'])
                elif re == 6:
                    self.rank_default_init['semaphore'] = self.check.input('设置最大同时下载数', check_mode=CHECK_MODE_INT_RANGE,
                                                                           min_val=1)

                n = self.check.input('\n是否修改完毕?修改完毕按Y,继续修改按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                     str_list=['Y', 'y', 'N', 'n'])
                if n in ['Y', 'y']:
                    return self.rank_default_init

    def init_tags_print(self):
        display_head("标签下载模式")

        print('1. 是否对收藏数进行筛选,默认开启')
        print('2. 是否按照最新排序,默认最新排序')
        print('3. 是否需要指定页数,默认为第一页')
        print('4. 是否启用部分标签,默认开启')
        print("5. 是否需要选取动图,默认关闭")
        print('6. 是否启用清晰度筛选,默认关闭')
        print('7. 是否对横纵比进行筛选,默认关闭')
        print('8. 是否需要指定储存文件夹,默认文件夹为tags文件夹')
        print('9. 是否需要修改最大同时下载数量,默认为10')

        juge = self.check.input('\n使用默认方式请按Y,需要更改请按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                str_list=['Y', 'y', 'N', 'n'])
        if juge in ['Y', 'y']:
            return None
        elif juge in ['N', 'n']:
            while True:
                re = self.check.input('选择需要更改的内容', check_mode=CHECK_MODE_INT_RANGE, min_val=1, max_val=9)
                if re == 1:
                    self.tags_default_init['bookmarkCount'] = not self.tags_default_init['bookmarkCount']
                    print('指定收藏数模式已开启') if self.tags_default_init['bookmarkCount'] else print('指定收藏数模式已关闭')
                elif re == 2:
                    self.tags_default_init['order'] = not self.tags_default_init['order']
                    print('已按最新排序') if self.tags_default_init['order'] else print('已按最旧排序')
                elif re == 3:
                    self.tags_default_init['page'] = not self.tags_default_init['page']
                    print('指定页码范围模式已开启') if self.rank_default_init['page'] else print('指定页码范围模式已关闭')
                elif re == 4:
                    self.tags_default_init['sectionTag'] = not self.tags_default_init['sectionTag']
                    print('部分标签模式已开启') if self.tags_default_init['sectionTag'] else print('部分标签模式已关闭')
                elif re == 5:
                    self.tags_default_init['illType'] = not self.tags_default_init['illType']
                    print('只对插画进行选择') if self.tags_default_init['illType'] else print('对插画、动图进行选择')
                elif re == 6:
                    self.tags_default_init['resolution'] = not self.tags_default_init['resolution']
                    print('分辨率筛选模式已开启') if self.tags_default_init['resolution'] else print('分辨率筛选模式已关闭')
                elif re == 7:
                    self.tags_default_init['ratio'] = not self.tags_default_init['ratio']
                    print('方向选择已开启') if self.tags_default_init['ratio'] else print('方向选择已关闭')
                elif re == 8:
                    self.tags_default_init['save_folder'] = input('输入储存文件夹')
                elif re == 9:
                    self.tags_default_init['semaphore'] = self.check.input('设置最大同时下载数', check_mode=CHECK_MODE_INT_RANGE,
                                                                           min_val=1)

                n = self.check.input('\n是否修改完毕?修改完毕按Y,继续修改按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                     str_list=['Y', 'y', 'N', 'n'])
                if n in ['Y', 'y']:
                    return self.tags_default_init

    def init_id_print(self):
        display_head("id下载模式")

        print('1. 是否需要通过id_download.txt文件进行下载,默认关闭')
        print('2. 是否需要修改文件读取路径,默认读取路径为./id_download.txt')
        print('3. 是否需要指定储存文件夹,默认文件夹为id_download文件夹')
        print('4. 是否需要修改最大同时下载数量,默认为10')
        juge = self.check.input('\n使用默认方式请按Y,需要更改请按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                str_list=['Y', 'y', 'N', 'n'])
        if juge in ['Y', 'y']:
            return None
        elif juge in ['N', 'n']:
            while True:
                re = self.check.input('选择需要更改的内容', check_mode=CHECK_MODE_INT_RANGE, min_val=1, max_val=3)
                if re == 1:
                    self.id_default_init['idlist'] = not self.id_default_init['idlist']
                    print('根据文件中的id批量下载模式已开启') if self.id_default_init['idlist'] else print('根据文件中的id批量下载模式已关闭')
                elif re == 2:
                    self.id_default_init['read_folder'] = input('输入要读取的txt文件')
                elif re == 3:
                    self.id_default_init['save_folder'] = input('输入储存文件夹')
                elif re == 4:
                    self.id_default_init['semaphore'] = self.check.input('设置最大同时下载数', check_mode=CHECK_MODE_INT_RANGE,
                                                                         min_val=1)
                n = self.check.input('\n是否修改完毕?修改完毕按Y,继续修改按N\n输入:', check_mode=CHECK_MODE_STR_LIST,
                                     str_list=['Y', 'y', 'N', 'n'])
                if n in ['Y', 'y']:
                    return self.tags_default_init


class Menu:
    result = []

    def __init__(self, modeset, mode=None):
        self.check = CheckInputFormat()
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
            # todo 菜单排行榜模式已完成
            self.pageList = self.__get_page_list() if modeset.page else ['&p=1']
            self.dateList = self.__get_data_list() if modeset.DateTime else "&date=" + (datetime.datetime.now() +
                                                                                        datetime.timedelta(
                                                                                            days=-2)).strftime(
                '%Y-%m-%d').replace('-', '')
            self.rank_mode = rank_mode[modeset.rank_mode]
            self.rank_content = rank_content[modeset.rank_content]
        elif mode == 'id':

            pass
        else:
            raise Exception('未输入mode参数')

    def __get_data_list(self):
        while True:
            start_day = self.check.input("输入开始日期(****-**-**):", CHECK_MODE_DATE)
            end_day = self.check.input("输入截止日期(****-**-**):", CHECK_MODE_DATE)
            datestart = datetime.datetime.strptime(start_day, '%Y-%m-%d')
            dateend = datetime.datetime.strptime(end_day, '%Y-%m-%d')
            if datestart >= dateend:
                print('检索时间不存在,重新输入')
            else:
                break
        date_mode = self.check.input("输入日期计算方式(day、weekly、monthly)", CHECK_MODE_STR_LIST,
                                     str_list=['day', 'weekly', 'monthly'])
        datelist = get_datelist(start_day, end_day, mode=date_mode)
        return datelist

    def __get_bookmark_count(self):
        num = self.check.input("输入最小收藏数量(整数)", CHECK_MODE_INT_RANGE)
        bookmarkCount = f"%20{num}users入り"
        return bookmarkCount

    def __get_resolution(self):
        print('选择分辨率要求:\n1.3000^2以上\n2.1000^2~3000^2\n3.1000^2以下(输入1 2 3)')
        d = {
            "1": "&wlt=3000&hlt=3000",
            "2": "&wlt=1000&wgt=2999&hlt=1000&hgt=2999",
            "3": "&wgt=999&hgt=999"
        }
        f = self.check.input("输入", CHECK_MODE_INT_RANGE, min_val=1, max_val=3)
        resolution = d[f'{f}']
        return resolution

    def __get_ratio(self):
        print('选择方向:\n1.横图\n2.纵图\n3.正方形')
        d = {
            "1": "&ratio=0.5",
            "2": "&ratio=-0.5",
            "3": "&ratio=0"
        }
        f = self.check.input("输入", CHECK_MODE_INT_RANGE, min_val=1, max_val=3)
        ratio = d[f'{f}']
        return ratio

    def __get_page_list(self):
        start_page = self.check.input("输入开始页码", CHECK_MODE_INT_RANGE, min_val=1)
        end_page = self.check.input("输入结束页码", CHECK_MODE_INT_RANGE, min_val=start_page)
        pageList = [f"&p={i}" for i in range(start_page, end_page + 1)]

        return pageList
