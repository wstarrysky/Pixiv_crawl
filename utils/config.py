import requests.adapters
from fake_useragent import UserAgent
import yaml

config = yaml.load(open('config.yaml', encoding='utf-8'), Loader=yaml.FullLoader)['setting']

CHECK_MODE_DATE = 0  # 检查日期模式
CHECK_MODE_INT_RANGE = 1  # 检查整数范围
CHECK_MODE_STR_LIST = 2  # 检查字符串

username = config['username']
password = config['password']
cookie = config['cookie']

requests.adapters.DEFAULT_RETRIES = 3  # 设置默认重连次数
# print(f"{bool(config['UA'])}")
if config['UA'] == True:
    ua = UserAgent()
    # 随机UA设置
    headers = {
        'Referer': "https://www.pixiv.net",
        'Connection': 'close',
        'User-Agent': str(ua.random),
        'username': username, 'password': password,
        'Cookie': cookie
    }
else:
    # 非随机UA设置
    headers = {
        'Referer': "https://www.pixiv.net",
        'Connection': 'close',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'username': username, 'password': password,
        'Cookie': cookie
    }
"************************同步设置*********************************"
proxies = {'http': config['proxy'], 'https': config['proxy']}

'''************************异步设置******************************'''
Pixiv = "https://www.pixiv.net/"
proxy = config['proxy']
cookies = {'cookie': config['cookie']}

'''*********************************************************'''
"""
排行榜模式  标签模式  收藏模式
"""
mode = ['rank',
        'tags',
        'bookmark'
        ]

'''*********************************************************'''

TAGS_URL = "https://www.pixiv.net/tags/"

page = f"&p={3}"
"""
每日排行榜  每周排行榜   每月排行榜
"""
rank_mode = {
    "今日": "?mode=daily&amp;ref=rn-h-day-3",
    "本周": "?mode=weekly&amp;ref=rn-h-week-3",
    "本月": "?mode=monthly&amp;ref=rn-h-month-3",
    "新人": "?mode=rookie&amp;ref=rn-h-rookie-3",
    "受男性欢迎": "?mode=male&amp;ref=rn-h-male-3",
    "受女性欢迎": "?mode=female&amp;ref=rn-h-female-3"
}

"""
综合内容  插画内容   动图内容
"""
rank_content = {
    "all": "",
    "illustration": "&content=illust",
    "gif": "&content=ugoira"
}

rank_ill_tag = {
    "今日": "?mode=daily&amp;ref=rn-h-day-3",
    "本周": "?mode=weekly&amp;ref=rn-h-week-3",
    "本月": "?mode=monthly&amp;ref=rn-h-month-3",
    "新人": "?mode=rookie&amp;ref=rn-h-rookie-3"
}

"""**********************************bilibili设置*****************************"""
bilibili_headers = {
    "Cookie": "_uuid=68AA8BB9-4B82-4B28-0417-60EDAC5B71BF84963infoc;buvid3=C8F261A5-6BE3-4EB4-9180-279D78A149FA167629infoc;blackside_state=1;rpdid=|(kJYkJ)|)k|0J'uYkYuRJ~|Y;buvid_fp=C8F261A5-6BE3-4EB4-9180-279D78A149FA167629infoc;SESSDATA=9b902ee1%2C1641695716%2C491e4%2A71;bili_jct=72d5d9b919e20318c3a32b56233211c0;DedeUserID=238243338;DedeUserID__ckMd5=f4f186d0158f567a;sid=72v5q4b9;buvid_fp_plain=C8F261A5-6BE3-4EB4-9180-279D78A149FA167629infoc;CURRENT_BLACKGAP=1;fingerprint3=de57863205185a44374ecf9df14959df;fingerprint=9f3452bb3d88660090a78afef30d197c;fingerprint_s=43bc90f92e501ebe0c6fe17fb3db84fe;LIVE_BUVID=AUTO6016293829041128;CURRENT_QUALITY=120;CURRENT_FNVAL=976;bsource=search_baidu;PVID=1;bp_video_offset_238243338=591665168459948793;video_page_version=v_old_home;innersign=0;i-wanna-go-back=1;b_ut=6;b_lsid=A3C1F1FA_17D83E2B031",
    "pragma": "no-cache",
    "referer": "https://space.bilibili.com/22396693/article",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.45Safari/537.36",
}
