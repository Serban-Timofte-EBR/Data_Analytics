# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'exemplu_designer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(772, 351)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.buton_citire = QPushButton(self.centralwidget)
        self.buton_citire.setObjectName(u"buton_citire")
        self.buton_citire.setGeometry(QRect(30, 30, 221, 41))
        self.lista_selectie_variabile = QListWidget(self.centralwidget)
        self.lista_selectie_variabile.setObjectName(u"lista_selectie_variabile")
        self.lista_selectie_variabile.setGeometry(QRect(30, 100, 256, 192))
        self.buton_afisare = QPushButton(self.centralwidget)
        self.buton_afisare.setObjectName(u"buton_afisare")
        self.buton_afisare.setGeometry(QRect(300, 30, 201, 41))
        self.out = QTextEdit(self.centralwidget)
        self.out.setObjectName(u"out")
        self.out.setGeometry(QRect(300, 100, 441, 191))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 772, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buton_citire.setText(QCoreApplication.translate("MainWindow", u"Citire fisier", None))
        self.buton_afisare.setText(QCoreApplication.translate("MainWindow", u"Afisare tabel", None))
    # retranslateUi


class Frame(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Frame, self).__init__()
        self.setupUi(self)
        self.buton_citire.clicked.connect(self.citire_fisier)
        self.buton_afisare.clicked.connect(self.afisare_tabel)

    def citire_fisier(self):
        dialog = QFileDialog(directory=".")
        dialog.exec_()
        fisiere = dialog.selectedFiles()
        self.t = pd.read_csv(fisiere[0])
        variabile = list(self.t)
        self.lista_selectie_variabile.clear()
        for v in variabile:
            item = QListWidgetItem(self.lista_selectie_variabile)
            self.lista_selectie_variabile.setItemWidget(item, QCheckBox(v))

    def afisare_tabel(self):
        variabile_selectate = []
        for i in range(self.lista_selectie_variabile.count()):
            item = self.lista_selectie_variabile.item(i)
            check = self.lista_selectie_variabile.itemWidget(item)
            assert isinstance(check, QCheckBox)
            if check.isChecked():
                variabile_selectate.append(check.text())
        self.out.append(",".join(variabile_selectate))
        for i in range(len(self.t)):
            self.out.append(",".join(str(j) for j in self.t[variabile_selectate].iloc[i, :]))


aplicatie = QApplication(sys.argv)
main_frame = Frame()
main_frame.show()
aplicatie.exec_()
