import copy
import datetime
import re

from utils import *
import time


class TagsMode:
    # todo 标签下载模式在此文件
    def __init__(self, rm, rc, d, p, sp='img', lc=None, res=None):
        self.save_path = sp
        self.page = p
        self.d = d
        self.date = "&date=" + (datetime.datetime.now() +
                                datetime.timedelta(days=-1)).strftime('%Y-%m-%d').replace('-', '')
        self.url = rank_url + \
                   rank_mode[rm] + \
                   rank_content[rc]
    def paser_tags_page(self):
        pass