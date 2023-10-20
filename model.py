import os
import shutil
from PIL import Image
import cv2
from PyQt5 import QtGui
import numpy as np
from PyQt5.QtWidgets import QFileDialog
from tensorflow.keras.models import load_model


class Model:

    def __init__(self):
        self.R = 2 ** 3
        self.process_path = ""
        self.save_path = ""
        self.dict1 = {}
        self.work_dir = os.getcwd()
        self.pic_1 = os.path.join(self.work_dir, "res/view_images/example.png")
        self.pic_2 = os.path.join(self.work_dir, "res/view_images/example2.png")
        self.picR_1 = os.path.join(self.work_dir, "res/view_images/dp1.png")
        self.picR_2 = os.path.join(self.work_dir, "res/view_images/dp2.png")
        self.mulpicR_1 = os.path.join(self.work_dir, "res/view_images/mp1.png")
        self.mulpicR_2 = os.path.join(self.work_dir, "res/view_images/mp2.png")

    def selectFile(self,view):
        # 前处理
        if os.path.exists(self.pic_1):
            os.remove(self.pic_1)
        if os.path.exists(self.pic_2):
            os.remove(self.pic_2)
        self.img_path = ""
        view.lineEdit.setText("")
        view.label.setPixmap(QtGui.QPixmap(""))
        view.label_2.setPixmap(QtGui.QPixmap(""))
        # 读文件
        self.img_path, filetype = QFileDialog.getOpenFileName(None, "选择路径", os.getcwd(), "Image Files(*.jpg *.png)")
        if self.img_path == "":
            print("未选择任何文件！！")
        else:
            try:
                # 处理文件
                img = Image.open(self.img_path)
                img.save(self.pic_1)
                height = img.size[1]
                width = img.size[0]
                x = int(600 * (height/width))
                img = img.resize((600, x), Image.ANTIALIAS)
                img.save(self.pic_2)
                view.lineEdit.setText(self.img_path)
                # shutil.copy(self.img_path, self.pic_1)
                # outfile, get_size = self.compress_image(self.pic_1,
                                                        # pic_2)
                # self.resize_image(self.pic_1, x_s=200)
                # view.label.setPixmap(QtGui.QPixmap(pic_2))
                view.label.setPixmap(QtGui.QPixmap(self.pic_2))
                print(self.img_path)
            except Exception as e:
                print(e)
    # 选择图片所在文件夹
    def selectProcessFolder(self,view):
        view.lineEdit_2.setText("")
        self.process_path = ""
        self.process_path = QFileDialog.getExistingDirectory(None, "选择文件夹", os.getcwd())
        if self.process_path == "":
            print("未选择文件夹")
        else:
            # 重命名图片
            view.lineEdit_2.setText(self.process_path)
            print("选择成功")


    def selectFolder(self,view):
        try:
            self.save_path = ""
            view.lineEdit_3.setText("")
            self.save_path = QFileDialog.getExistingDirectory(None, "选择文件夹", os.getcwd())
            if self.save_path == "":
                print("未选择文件夹")
            else:
                view.lineEdit_3.setText(self.save_path)
        except Exception as e:
            print(e)

    def predict(self,view):
        if os.path.exists(self.picR_1):
            os.remove(self.picR_1)
        if os.path.exists(self.picR_2):
            os.remove(self.picR_2)
        try:
            model = load_model('model.h5')
            filePath = self.pic_1
            img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
            # img = cv2.imread(self.pic_1)  # 从内存数据读入图片
            print("****************************")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # perform brightness correction in tiles
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
            img = clahe.apply(img)

            img_predict = cv2.resize(img, (img.shape[1] // self.R * self.R, img.shape[0] // self.R * self.R),
                                     interpolation=cv2.INTER_AREA)
            img_predict = np.reshape(img_predict, (1, img_predict.shape[0], img_predict.shape[1], 1))
            img_predict = img_predict.astype(np.float32) * 0.003383
            result = model.predict(img_predict, batch_size=1)[0]

            img_res = (result - np.mean(result) + 1.) * 255
            img_res = cv2.resize(img_res, (img.shape[1], img.shape[0]))
            out_dir = os.path.join(self.work_dir, "output")
            cv2.imencode(".png", img_res)[1].tofile(
                os.path.join(out_dir, self.img_path.split("/")[-1]))
            # 处理文件
            shutil.copy(os.path.join(out_dir, self.img_path.split('/')[-1]),
                        self.picR_1)
            # outfile, get_size = self.compress_image(picR_1,
            #                                         picR_2)
            imglas = Image.open(self.picR_1)
            height = imglas.size[1]
            width = imglas.size[0]
            x = int(600 * (height/width))
            imglas = imglas.resize((600, x), Image.ANTIALIAS)
            imglas.save(self.picR_2)
            # self.resize_image(picR_1, x_s=200)
            view.label_2.setPixmap(QtGui.QPixmap(self.picR_2))
            print("finish process single picture~")
            # cv2.imwrite(os.path.join('./output', "".join([self.img_path.split("/")[-1].replace(self.img_path.split("/")[-1].split(".")[-1],""), "jpg"])), img_res)
        except Exception as e:
            print(e)

    def mulPredict(self,view):
        try:
            if os.path.exists(self.mulpicR_1):
                os.remove(self.mulpicR_1)
            if os.path.exists(self.mulpicR_2):
                os.remove(self.mulpicR_2)
            if self.process_path == "" or self.save_path == "":
                print("未选择好文件夹")
            else:
                print("start...")
                self.main(view)
                print("finish process mul picture~")
        except Exception as e:
            print(e)

    # # 将process 文件夹的文件由中文名改为英文名
    # def method1(self):
    #     path = self.process_path
    #     # print(os.listdir(path))
    #     i = 1
    #     for file in os.listdir(path):
    #         print(file)
    #         file_path = os.path.join(path, file)
    #         self.dict1["s" + i.__str__()] = file.split(".")[0]
    #
    #         file_new = file.replace(
    #             file.replace(file.split(".")[-1], "")[0:len(file.replace(file.split(".")[-1], "")) - 1],
    #             "s" + i.__str__())
    #         file_new_path = os.path.join(path, file_new)
    #         os.rename(file_path, file_new_path)
    #         i += 1
    #
    #     filename = os.path.join(self.work_dir, "name.txt")
    #     with open(filename, 'w', encoding='utf-8') as f:
    #         for item in self.dict1.items():
    #             f.write(item[0] + ":" + item[1])
    #             f.write("\n")
    #             print(item)
    #
    # # 将process 文件夹的文件由英文名还原为中文名
    # def method2(self):
    #     path = self.process_path
    #     j = 1
    #     for file in os.listdir(path):
    #         # print(file)
    #         file_path = os.path.join(path, file)
    #         key = file.split(".")[0]
    #         ori_path = os.path.join(path, file.replace(key, self.dict1.get(key)))
    #         os.rename(file_path, ori_path)
    #         j += 1

    def main(self,view1):
        model = load_model(os.path.join(self.work_dir, "model.h5"))
        try:
            for root, dirs, files in os.walk(self.process_path, topdown=False):
                for name in files:
                    # print(os.path.join(root, name))
                    filePath = os.path.join(root, name)
                    # print(filePath)
                    im = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
                    cv2.imencode('.'+name.split('.')[-1], im)[1].tofile(self.mulpicR_1)
                    # 处理图片----------------------------------------------------
                    imglas1 = Image.open(self.mulpicR_1)
                    height = imglas1.size[1]
                    width = imglas1.size[0]
                    x = int(600 * (height / width))
                    imglas1 = imglas1.resize((600, x), Image.ANTIALIAS)
                    imglas1.save(self.mulpicR_1)
                    # ************************************************************
                    view1.label.setPixmap(QtGui.QPixmap(self.mulpicR_1))
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

                    # perform brightness correction in tiles
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
                    im = clahe.apply(im)

                    im_predict = cv2.resize(im, (im.shape[1] // self.R * self.R, im.shape[0] // self.R * self.R),
                                            interpolation=cv2.INTER_AREA)
                    im_predict = np.reshape(im_predict, (1, im_predict.shape[0], im_predict.shape[1], 1))
                    # im_predict = ((im_predict/255)*220)/255
                    im_predict = im_predict.astype(np.float32) * 0.003383

                    result = model.predict(im_predict, batch_size=4)[0]

                    im_res = (result - np.mean(result) + 1.) * 255
                    im_res = cv2.resize(im_res, (im.shape[1], im.shape[0]))
                    # cv2.imwrite(self.mulpicR_2, im_res)
                    cv2.imencode('.'+name.split('.')[-1], im_res)[1].tofile(self.mulpicR_2)

                    # 处理图片----------------------------------------------------
                    imglas2 = Image.open(self.mulpicR_2)
                    height2 = imglas2.size[1]
                    width2 = imglas2.size[0]
                    x2 = int(600 * (height2 / width2))
                    imglas2 = imglas2.resize((600, x2), Image.ANTIALIAS)
                    imglas2.save(self.mulpicR_2)
                    view1.label_2.setPixmap(QtGui.QPixmap(self.mulpicR_2))
                    img_new_path = os.path.join(self.save_path, name)
                    # cv2.imencode('.'+name.split('.')[-1], im_res)[1].tofile(img_new_path)
                    cv2.imencode('.'+name.split('.')[-1], im_res)[1].tofile(img_new_path)
        except Exception as e:
            print(e)
        # finally:
        #     os.remove(os.path.join(r, n))
