# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a:\3. C4-核酸检测信息自动化分析系统\TI4ALL-main7-2\src\gui\SettingWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName("SettingWindow")
        SettingWindow.resize(307, 300)
        self.centralwidget = QtWidgets.QWidget(SettingWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget_4)
        self.label_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_2.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.widget_2)
        self.radioButton_4.setObjectName("radioButton_4")
        self.horizontalLayout_2.addWidget(self.radioButton_4)
        self.gridLayout_2.addWidget(self.widget_2, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_4)
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_4)
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_5 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.horizontalLayout.addWidget(self.radioButton_5)
        self.radioButton_6 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_6.setEnabled(True)
        self.radioButton_6.setChecked(False)
        self.radioButton_6.setObjectName("radioButton_6")
        self.horizontalLayout.addWidget(self.radioButton_6)
        self.gridLayout_2.addWidget(self.widget, 1, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.widget_4)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.widget_3)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_3.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget_3)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_3.addWidget(self.radioButton_2)
        self.gridLayout_2.addWidget(self.widget_3, 3, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.widget_4)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_2, 4, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget_6 = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.confirm = QtWidgets.QPushButton(self.widget_6)
        self.confirm.setObjectName("confirm")
        self.horizontalLayout_4.addWidget(self.confirm)
        self.cancel = QtWidgets.QPushButton(self.widget_6)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_4.addWidget(self.cancel)
        self.verticalLayout.addWidget(self.widget_6)
        SettingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingWindow.setWindowTitle(_translate("SettingWindow", "高级设置（尚未支持）"))
        self.label_5.setText(_translate("SettingWindow", "OCR模型版本："))
        self.label_2.setText(_translate("SettingWindow", "启用辅助信息："))
        self.label.setText(_translate("SettingWindow", "语言："))
        self.radioButton_3.setText(_translate("SettingWindow", "是"))
        self.radioButton_4.setText(_translate("SettingWindow", "否"))
        self.label_3.setText(_translate("SettingWindow", "开启mkldnn："))
        self.label_4.setText(_translate("SettingWindow", "使用tensorrt："))
        self.radioButton_5.setText(_translate("SettingWindow", "是"))
        self.radioButton_6.setText(_translate("SettingWindow", "否"))
        self.comboBox.setItemText(0, _translate("SettingWindow", "中文（简体）"))
        self.radioButton.setText(_translate("SettingWindow", "是"))
        self.radioButton_2.setText(_translate("SettingWindow", "否"))
        self.comboBox_2.setItemText(0, _translate("SettingWindow", "PP-OCRv2（建议）"))
        self.comboBox_2.setItemText(1, _translate("SettingWindow", "PP-OCR"))
        self.comboBox_2.setItemText(2, _translate("SettingWindow", "PP-OCRv3"))
        self.confirm.setText(_translate("SettingWindow", "确认"))
        self.cancel.setText(_translate("SettingWindow", "取消"))

