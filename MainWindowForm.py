# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiMainWindowForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowForm(object):
    def setupUi(self, MainWindowForm):
        MainWindowForm.setObjectName("MainWindowForm")
        MainWindowForm.resize(196, 563)
        self.centralwidget = QtWidgets.QWidget(MainWindowForm)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 160, 176))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name_game = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_name_game.setObjectName("label_name_game")
        self.verticalLayout.addWidget(self.label_name_game)
        self.btn_start_game = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_start_game.setObjectName("btn_start_game")
        self.verticalLayout.addWidget(self.btn_start_game)
        self.btn_settings = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_settings.setObjectName("btn_settings")
        self.verticalLayout.addWidget(self.btn_settings)
        self.btn_guide = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_guide.setObjectName("btn_guide")
        self.verticalLayout.addWidget(self.btn_guide)
        self.btn_info = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_info.setObjectName("btn_info")
        self.verticalLayout.addWidget(self.btn_info)
        self.btn_close = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout.addWidget(self.btn_close)
        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(10, 200, 151, 251))
        self.label_info.setText(">>>")
        self.label_info.setObjectName("label_info")
        self.label_info.resize(self.label_info.sizeHint())
        MainWindowForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 196, 21))
        self.menubar.setObjectName("menubar")
        MainWindowForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowForm)
        self.statusbar.setObjectName("statusbar")
        MainWindowForm.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindowForm)
        QtCore.QMetaObject.connectSlotsByName(MainWindowForm)

    def retranslateUi(self, MainWindowForm):
        _translate = QtCore.QCoreApplication.translate
        MainWindowForm.setWindowTitle(_translate("MainWindowForm", "Apocalypse"))
        self.label_name_game.setText(_translate("MainWindowForm", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">Apocalypse</span></p></body></html>"))
        self.btn_start_game.setText(_translate("MainWindowForm", "Начать новую игру"))
        self.btn_settings.setText(_translate("MainWindowForm", "Настройки"))
        self.btn_guide.setText(_translate("MainWindowForm", "ГИД"))
        self.btn_info.setText(_translate("MainWindowForm", "О программе"))
        self.btn_close.setText(_translate("MainWindowForm", "Выход"))
