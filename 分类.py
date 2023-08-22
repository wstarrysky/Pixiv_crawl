# 根据图片横竖比进行分类
import os
import shutil
from PIL import Image

def fenlei(folder):
    if not os.path.exists(os.path.join(folder, '横图')):
        os.makedirs(os.path.join(folder, '横图'))
    if not os.path.exists(os.path.join(folder, '竖图')):
        os.makedirs(os.path.join(folder, '竖图'))
    file_list = os.listdir(folder)
    for file in file_list:
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):  # Make sure the item is a file
            img = Image.open(file_path)
            width, height = img.size
            if width > height:
                shutil.copy(file_path, os.path.join(folder, '横图', file))
            else:
                shutil.copy(file_path, os.path.join(folder, '竖图', file))

if __name__ == '__main__':
    fenlei(r'rank/20230821')
