import sys

from PyQt5 import QtWidgets

from view_login import Ui_MainWindow as login
from view_main import Ui_MainWindow as mainw
import model


class LoginWindow(QtWidgets.QMainWindow, login):  # 主界面新建的类
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)


class mainWindow(QtWidgets.QMainWindow, mainw):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)


class Controller:
    def __init__(self):
        # 登录窗口
        self.m1 = LoginWindow()
        # 主窗口
        self.m2 = mainWindow()
        # 方法函数
        self.model = model.Model()
        # 信号槽信号绑定
        self.m1.pushButton.clicked.connect(self.change)

    def run(self):
        self.m1.show()
        self.m2.hide()

    def change(self):
        self.m1.close()
        self.m2.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ctr = Controller()
    ctr.run()
    sys.exit(app.exec_())
    # try:
    #     app = QtWidgets.QApplication(sys.argv)
    #     ctr = Controller()
    #     ctr.run()
    #     sys.exit(app.exec_())
    # except Exception as e:
    #     print(e)
