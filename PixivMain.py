import re
from mode import ToRankMode,TagsMode
import argparse

from mode.IDMode import IDMode
from utils.common import *
from bs4 import BeautifulSoup



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Pixiv懒人脚本")
    parser.add_argument('-m', '--mode', type=str, required=True, help="['rank','tags','id']")
    args = parser.parse_args()

    if args.mode == "rank":
        rank = ToRankMode()
    elif args.mode == "tags":
        tags = TagsMode()
    elif args.mode == "id":
        id = IDMode()