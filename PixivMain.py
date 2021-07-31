import re
from mode import ToRankMode,TagsMode
import argparse
from utils.common import *
from bs4 import BeautifulSoup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pixiv懒人脚本")
    parser.add_argument('-m', '--mode', type=str, required=True, help="['rank','tags','bookmark','id']")
    args = parser.parse_args()

    if args.mode == "rank":
        rank = ToRankMode()
    elif args.mode == "tags":
        tags = TagsMode()
    elif args.mode == "bookmark":
        print("目前只开发了排行榜模式和标签下载模式哦,收藏夹模式尚待开发")
        exit()
    elif args.mode == "id":
        print("目前只开发了排行榜模式和标签下载模式哦,收藏夹模式尚待开发")
        exit()
