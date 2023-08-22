from mode import ToRankMode, TagsMode
from mode.BiliBiliMode import BilibiliMode
from mode.IDMode import IDMode
from utils import display_head

if __name__ == "__main__":
    Model_options = ['rank', 'tags', 'id']
    options = {
        'rank': ToRankMode,
        "tags": TagsMode,
        "id": IDMode,
    }
    try:
        while True:
            mode = str(input(f"选择使用模式{Model_options}\n输入:"))
            if mode not in Model_options:
                print('模式选择错误,重新输入')
            else:
                break
        option = options[mode]
        run  = option()
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
