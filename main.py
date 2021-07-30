import re
from mode import ToRankMode,TagsMode
import argparse
from utils.common import *
from bs4 import BeautifulSoup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pixiv懒人脚本")
    parser.add_argument('-m', '--mode', type=str, required=True, help="['rank','tags','bookmark','id']")
    '''************************global   setting******************************************'''

    parser.add_argument('-res', '--resolution', type=str, default=None, help="1080  2k  4k (是否对分辨率有要求) ")
    parser.add_argument('-bmc', '--bookmark_count', type=int, default=None, help="the count of bookmark")
    parser.add_argument('-lc', '--like_count', type=int, default=1000, help="the count of like count(是否对喜欢数有要求)")
    '''************************rank_mode   setting******************************************'''
    parser.add_argument('-rm', '--rank_mode', type=str, default='受男性欢迎', help="['今日','本周','本月','新人',"
                                                                              "'受男性欢迎','受女性欢迎'](只有选择综合内容"
                                                                              "才有(受男/女性欢迎模式)")
    parser.add_argument('-rc', '--rank_content', type=str, default='all', help="['all','illustration','gif']")
    parser.add_argument('-d', '--datetime', type=bool, default=True, help="是否指定日期下载")
    parser.add_argument('-p', '--page', type=tuple, default=None, help="(开始页,截止页)")
    '''************************save  setting******************************************'''
    parser.add_argument('-sp', '--save_path', type=str, default="img", help="the end day")
    args = parser.parse_args()

    if args.mode == "rank":
        rank = ToRankMode(args.rank_mode, args.rank_content, args.datetime,
                          args.page, args.save_path, args.like_count, args.resolution)
    elif args.mode == "tags":
        tags = TagsMode(args.rank_mode, args.rank_content, args.datetime,
                          args.page, args.save_path, args.like_count, args.resolution)
        exit()
    elif args.mode == "bookmark":
        print("目前只开发了排行榜模式哦,收藏夹模式尚待开发")
        exit()
    elif args.mode == "id":
        print("目前只开发了排行榜模式哦,图片id模式尚待开发")
        exit()
