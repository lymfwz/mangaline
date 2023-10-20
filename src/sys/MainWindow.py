# pyqt5主窗口
from PyQt5 import QtWidgets, QtCore, QtGui
# 导包
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
import sys

# 写一个带主函数、登录窗口、主窗口的pyqt5程序
# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.setWindowTitle('主窗口')
        self.pushButton.clicked.connect(self.close)

    def setupUi(self):
        self.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "退出系统"))

# 登录窗口
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi()
        self.setWindowTitle('登录窗口')
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.close)

    # ui界面带用户密码输入框、登录退出按钮
    def setupUi(self):
        self.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 100, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    # def setupUi(self):
    #     self.resize(400, 300)
    #     # 固定大小
    #     self.setFixedSize(self.width(), self.height())
    #
    #     self.centralwidget = QtWidgets.QWidget(self)
    #     self.centralwidget.setObjectName("centralwidget")
    #     self.pushButton = QtWidgets.QPushButton(self.centralwidget)
    #     self.pushButton.setGeometry(QtCore.QRect(100, 100, 75, 23))
    #     self.pushButton.setObjectName("pushButton")
    #     self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
    #     self.pushButton_2.setGeometry(QtCore.QRect(200, 100, 75, 23))
    #     self.pushButton_2.setObjectName("pushButton_2")
    #     self.setCentralWidget(self.centralwidget)
    #     self.statusbar = QtWidgets.QStatusBar(self)
    #     self.statusbar.setObjectName("statusbar")
    #     self.setStatusBar(self.statusbar)
    #
    #     self.retranslateUi()
    #     QtCore.QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def login(self):
        self.close()
        self.m = MainWindow()
        self.m.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "退出"))


# 主函数
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())