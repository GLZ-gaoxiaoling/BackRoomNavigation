# -*- coding: utf-8 -*-
import time

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from Navigation.path_finder import bfs_shortest_path
from Navigation.graph_loader import get_graph_from_db
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.graph = get_graph_from_db('level_exit.db')

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(491, 761)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(110, 170, 241, 71))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(110, 290, 241, 71))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 660, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.centerCtrl)

        self.label = QtWidgets.QTextEdit(self.centralwidget)
        self.label.setReadOnly(True)
        self.label.setGeometry(QtCore.QRect(110, 380, 241, 151))
        self.label.setFont(QtGui.QFont('Adobe Devanagari', 10))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 491, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.menu.addAction(self.actionSetting)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def centerCtrl(self):
        self.label.setText("PARDON MADE")
        kono_location = self.textEdit.toPlainText()
        after_location = self.textEdit_2.toPlainText()

        self.label.setText("后室导航中...")
        shortest_path = bfs_shortest_path(self.graph, kono_location, after_location)
        if shortest_path is None:
            self.label.setText("无法到达")
            return 0
        for  i in range(len(shortest_path)):
            shortest_path[i]="Level "+shortest_path[i]
        str_path = "->".join(map(str, shortest_path))
        self.label.setText(str_path)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "后室导航"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">当前所在层级</p></body></html>"))
        self.textEdit_2.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">预期抵达层级</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "开始导航"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.actionSetting.setText(_translate("MainWindow", "帮助"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())