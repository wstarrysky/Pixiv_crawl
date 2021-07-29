username = '2536187511'
password = '12345678Qwer..'
cookie = '62173541_1HKrL4dJ2vZcZ5b3EPvGO2vOHovNXtP7 '

headers = {
    'Referer': "https://www.pixiv.net/",  # p站需要开了请求头才能够进行下载
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 '
                  'Safari/537.36 LBBROWSER ',
    'username': username, 'password': password,
    'Cookie': cookie
}

proxies = {'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}
'''*********************************************************'''
Pixiv = "https://www.pixiv.net/"

'''*********************************************************'''
"""
排行榜模式  标签模式  收藏模式
"""
mode = ['rank',
        'tags',
        'bookmark'
        ]

'''*********************************************************'''
rank_url = "https://www.pixiv.net/ranking.php"

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
