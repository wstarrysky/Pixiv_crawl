from mode import ToRankMode, TagsMode
from mode.IDMode import IDMode
from utils import display_head

if __name__ == "__main__":
    try:
        while True:
            mode = str(input("选择使用模式 ['rank', 'tags', 'id']\n输入:"))
            if mode not in ['rank', 'tags', 'bookmark', 'id']:
                print('模式选择错误,重新输入')
            else:
                break
        if mode == "rank":
            rank = ToRankMode()
        elif mode == "tags":
            tags = TagsMode()
        elif mode == "id":
            id = IDMode()

        print("*******************************************************************")
        print("下载完成,按q键退出")
        while True:
            val = input('按q键退出')
            if val == 'q':
                break
        exit()
    except Exception as e:
        print(e)
        while True:
            val = input('按q键退出')
            if val == 'q':
                break
        exit()
