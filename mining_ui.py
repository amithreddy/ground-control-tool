# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mining.ui'
#
# Created: Sat Dec 20 17:48:15 2014
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName(_fromUtf8("window"))
        window.resize(800, 600)
        self.centralwidget = QtGui.QWidget(window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Views = QtGui.QWidget()
        self.Views.setObjectName(_fromUtf8("Views"))
        self.widget = QtGui.QWidget(self.Views)
        self.widget.setGeometry(QtCore.QRect(10, 11, 149, 341))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.t1 = QtGui.QLineEdit(self.widget)
        self.t1.setObjectName(_fromUtf8("t1"))
        self.verticalLayout_2.addWidget(self.t1)
        self.t2 = QtGui.QLineEdit(self.widget)
        self.t2.setObjectName(_fromUtf8("t2"))
        self.verticalLayout_2.addWidget(self.t2)
        self.t3 = QtGui.QLineEdit(self.widget)
        self.t3.setObjectName(_fromUtf8("t3"))
        self.verticalLayout_2.addWidget(self.t3)
        self.t4 = QtGui.QLineEdit(self.widget)
        self.t4.setObjectName(_fromUtf8("t4"))
        self.verticalLayout_2.addWidget(self.t4)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.b1 = QtGui.QLineEdit(self.widget)
        self.b1.setObjectName(_fromUtf8("b1"))
        self.verticalLayout_2.addWidget(self.b1)
        self.b2 = QtGui.QLineEdit(self.widget)
        self.b2.setObjectName(_fromUtf8("b2"))
        self.verticalLayout_2.addWidget(self.b2)
        self.b3 = QtGui.QLineEdit(self.widget)
        self.b3.setObjectName(_fromUtf8("b3"))
        self.verticalLayout_2.addWidget(self.b3)
        self.b4 = QtGui.QLineEdit(self.widget)
        self.b4.setObjectName(_fromUtf8("b4"))
        self.verticalLayout_2.addWidget(self.b4)
        self.submit = QtGui.QPushButton(self.widget)
        self.submit.setObjectName(_fromUtf8("submit"))
        self.verticalLayout_2.addWidget(self.submit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.widget1 = QtGui.QWidget(self.widget)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.horizontalLayout.addWidget(self.widget1)
        self.tabWidget.addTab(self.Views, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        window.setStatusBar(self.statusbar)

        self.retranslateUi(window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        window.setWindowTitle(_translate("window", "MainWindow", None))
        self.tabWidget.setToolTip(_translate("window", "<html><head/><body><p><br/></p></body></html>", None))
        self.label.setText(_translate("window", "Top", None))
        self.label_2.setText(_translate("window", "Bottom", None))
        self.submit.setText(_translate("window", "Submit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Views), _translate("window", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("window", "Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("window", "Page", None))

