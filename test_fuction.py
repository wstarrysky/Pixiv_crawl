import requests
import urllib3
from utils.config import *
url = 'https://www.pixiv.net/ajax/illust/91638841'
proxies = {'http': config['proxy'], 'https': config['proxy']}
headers = headers
print(headers)
res = requests.get(url=url, headers=headers, proxies=proxies)
print(res.json()['body']['urls']['original'])