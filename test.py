import os

import numpy as np
import cv2

def someblur(src, blursize=5):
    # dst = cv2.blur(src, (blursize, blursize))
    dst = cv2.GaussianBlur(src, (blursize, blursize), 1)
    return dst

def desharpen(src):
    blur = someblur(src, 5)
    dst = cv2.addWeighted(src, 0.5, blur, 0.5, 0)
    return dst

def quzao(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def ruihua(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 定义一个核
    dst = cv2.filter2D(image, -1, kernel=kernel)
    return dst

# 计算路径下的图片的个数
def count(path):
    i = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".png") or name.endswith(".jpg"):
                i += 1
    return i

# 清空路径图片
def clear(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name.endswith(".png") or name.endswith(".jpg"):
                os.remove(os.path.join(root, name))
    print("finish~")

if __name__ == '__main__':
    filePath = r"F:\Code\projects_2\qt_mvc-master\output\back压缩.png"
    img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    # print(img)
    ruihua_img = quzao(img)
    cv2.imencode(".png", ruihua_img)[1].tofile(os.path.join('output', filePath.split("\\")[-1]))
    # path = 'E:\download\秦腔\服装展图\服装展图'
    # # path1 = 'E:\download\秦腔\服装展图\服装展图'
    # # path1 = r"F:\Code\projects_2\线图\提取线图2"
    # for root, dirs, files in os.walk(path, topdown=False):
    #     for name in files:
    #         if name.split('.')[0].endswith('去噪锐化二值化提取线图'):
    #             if name.startswith('转化'):
    #
    #                 print(root)
    #                 print(name)
    #                 # os.remove(os.path.join(root,name))
    #                 new = name.replace("转化", "")
    #                 # print(new)
    #                 os.rename(os.path.join(root, name), os.path.join(root, new))


                # print(root.split('\\')[-1])
                # print(os.path.join(os.path.join(path1, root.split('\\')[-1]), name))
                # if not os.path.exists(os.path.join(path1, root.split('\\')[-1])):  # 判断文件夹是否已经存在
                #     os.mkdir(os.path.join(path1, root.split('\\')[-1]))
                # # # print(path1+root.split('\\')[-1])
                # # print(name)
                # filePath = os.path.join(root, name)
                # image = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
                # # cv2.imencode('.'+name.split('.')[-1], image)[1].tofile(os.path.join(os.path.join(path1, root.split('\\')[-1]), name.replace('去噪锐化提取线图',"去噪锐化二值化提取线图")))
                # cv2.imencode('.'+name.split('.')[-1], image)[1].tofile(os.path.join(root, name.replace('去噪锐化提取线图',"去噪锐化二值化提取线图")))
