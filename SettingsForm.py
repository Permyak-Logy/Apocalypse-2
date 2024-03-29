# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiSettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

NK_MAX_FOR_ENEMY = 16

class Ui_FormSettings(object):
    def setupUi(self, FormSettings):
        FormSettings.setObjectName("FormSettings")
        FormSettings.resize(385, 344)
        FormSettings.setAcceptDrops(False)
        self.formLayoutWidget = QtWidgets.QWidget(FormSettings)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 361, 160))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_2)
        
        self.checkBoxStraightForwardEnemy = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBoxStraightForwardEnemy.setEnabled(True)
        self.checkBoxStraightForwardEnemy.setChecked(True)
        self.checkBoxStraightForwardEnemy.setObjectName("checkBoxStraightForwardEnemy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBoxStraightForwardEnemy)
        self.countStraightForwardEnemies = QtWidgets.QSlider(self.formLayoutWidget)
        self.countStraightForwardEnemies.setMaximum(NK_MAX_FOR_ENEMY)
        self.countStraightForwardEnemies.setOrientation(QtCore.Qt.Horizontal)
        self.countStraightForwardEnemies.setObjectName("countStraightForwardEnemies")
        self.countStraightForwardEnemies.setProperty("value", 6)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.countStraightForwardEnemies)
        
        self.checkBoxStupidEnemy = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBoxStupidEnemy.setEnabled(True)
        self.checkBoxStupidEnemy.setChecked(True)
        self.checkBoxStupidEnemy.setObjectName("checkBoxStupidEnemy")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.checkBoxStupidEnemy)
        self.countStupidEnemies = QtWidgets.QSlider(self.formLayoutWidget)
        self.countStupidEnemies.setMaximum(NK_MAX_FOR_ENEMY)
        self.countStupidEnemies.setProperty("value", 6)
        self.countStupidEnemies.setOrientation(QtCore.Qt.Horizontal)
        self.countStupidEnemies.setObjectName("countStupidEnemies")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.countStupidEnemies)
        
        self.checkBoxSmartEnemy = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBoxSmartEnemy.setEnabled(True)
        self.checkBoxSmartEnemy.setChecked(True)
        self.checkBoxSmartEnemy.setObjectName("checkBoxSmartEnemy")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.checkBoxSmartEnemy)
        self.countSmartEnemies = QtWidgets.QSlider(self.formLayoutWidget)
        self.countSmartEnemies.setMaximum(NK_MAX_FOR_ENEMY)
        self.countSmartEnemies.setOrientation(QtCore.Qt.Horizontal)
        self.countSmartEnemies.setObjectName("countSmartEnemies")
        self.countSmartEnemies.setProperty("value", 1)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.countSmartEnemies)
        
        self.checkBoxSecretiveEnemy = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBoxSecretiveEnemy.setEnabled(True)
        self.checkBoxSecretiveEnemy.setChecked(True)
        self.checkBoxSecretiveEnemy.setObjectName("checkBoxSecretiveEnemy")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.checkBoxSecretiveEnemy)
        self.countSecretiveEnemies = QtWidgets.QSlider(self.formLayoutWidget)
        self.countSecretiveEnemies.setMaximum(NK_MAX_FOR_ENEMY)
        self.countSecretiveEnemies.setProperty("value", 2)
        self.countSecretiveEnemies.setOrientation(QtCore.Qt.Horizontal)
        self.countSecretiveEnemies.setObjectName("countSecretiveEnemies")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.countSecretiveEnemies)
        
        self.checkBoxTraps = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBoxTraps.setEnabled(True)
        self.checkBoxTraps.setChecked(True)
        self.checkBoxTraps.setObjectName("checkBoxTraps")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.checkBoxTraps)
        self.countTraps = QtWidgets.QSlider(self.formLayoutWidget)
        self.countTraps.setMaximum(25)
        self.countTraps.setProperty("value", 5)
        self.countTraps.setOrientation(QtCore.Qt.Horizontal)
        self.countTraps.setObjectName("countTraps")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.countTraps)
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(FormSettings)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 210, 351, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.editer_size_y = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.editer_size_y.setMinimum(4)
        self.editer_size_y.setObjectName("editer_size_y")
        self.horizontalLayout.addWidget(self.editer_size_y)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.editer_size_x = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.editer_size_x.setMinimum(5)
        self.editer_size_x.setObjectName("editer_size_x")
        self.horizontalLayout.addWidget(self.editer_size_x)
        self.label_5 = QtWidgets.QLabel(FormSettings)
        self.label_5.setGeometry(QtCore.QRect(130, 190, 111, 16))
        self.label_5.setObjectName("label_5")
        self.btn_ok = QtWidgets.QPushButton(FormSettings)
        self.btn_ok.setGeometry(QtCore.QRect(300, 310, 75, 23))
        self.btn_ok.setObjectName("btn_ok")
        self.label_6 = QtWidgets.QLabel(FormSettings)
        self.label_6.setGeometry(QtCore.QRect(10, 260, 291, 71))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(FormSettings)
        QtCore.QMetaObject.connectSlotsByName(FormSettings)

    def retranslateUi(self, FormSettings):
        _translate = QtCore.QCoreApplication.translate
        FormSettings.setWindowTitle(_translate("FormSettings", "Настройки"))
        self.label.setText(_translate("FormSettings", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Враги и ловушки</span></p></body></html>"))
        self.label_2.setText(_translate("FormSettings", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Количество</span></p></body></html>"))
        self.checkBoxStraightForwardEnemy.setText(_translate("FormSettings", "Прямоходящий"))
        self.checkBoxStupidEnemy.setText(_translate("FormSettings", "Глупый"))
        self.checkBoxSmartEnemy.setText(_translate("FormSettings", "Умный"))
        self.checkBoxSecretiveEnemy.setText(_translate("FormSettings", "Скрытный"))
        self.checkBoxTraps.setText(_translate("FormSettings", "Ловушки           "))
        self.label_3.setText(_translate("FormSettings", "По вертикали"))
        self.label_4.setText(_translate("FormSettings", "По горизонтали"))
        self.label_5.setText(_translate("FormSettings", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Размер карты</span></p></body></html>"))
        self.btn_ok.setText(_translate("FormSettings", "ОК"))
        self.label_6.setText(_translate("FormSettings", "<html><head/><body><p><span style=\" font-weight:600;\">Примечание:</span></p><p>Настройки вступают в силу после нажатия кнопки ОК</p><p>и старта новой игры</p></body></html>"))
