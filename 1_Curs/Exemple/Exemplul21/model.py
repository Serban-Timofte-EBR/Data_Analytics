import gui
import PySide2.QtWidgets as qw
from PySide2.QtCore import Qt
import pandas as pd


class model_class():
    def __init__(self):
        h_buton = 40
        stil1 = "color: rgb(0, 0, 255); font: 14pt \"Times New Roman\";"
        stil2 = "color: rgb(0, 0, 255); font: 12pt \"Times New Roman\";"

        self.variabile_selectate = []
        self.tabel_date = None
        self.date_citite = False

        self.model_creat = False

        self.b_citire = gui.Buton("Citire date", 300, h_buton, stil1, self.citire_fisier)
        self.c_variabila_index = qw.QComboBox()
        self.c_variabila_index.setStyleSheet(stil2)
        self.l_variabile_selectate = qw.QListWidget()
        self.l_variabile_selectate.setFixedSize(300, 300)
        self.l_variabile_selectate.setStyleSheet(stil2)
        self.l_variabile_selectate.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)
        self.ch_selectie_variabile = qw.QCheckBox("Selectie toate")
        self.ch_selectie_variabile.setStyleSheet(stil2)
        self.ch_selectie_variabile.stateChanged.connect(self.selectie_toate_variabilele)

        self.b_actiune1 = gui.Buton("Actiune 1", 200, h_buton, stil1, self.actiune1)
        # Alte butoane
        # ...

        layout_parametrii = qw.QVBoxLayout()
        layout_parametrii.addWidget(self.b_citire)
        formLayout = qw.QFormLayout()
        formLayout.addRow(gui.Eticheta("Variabila index:", stil=stil2), self.c_variabila_index)
        formLayout.addRow(gui.Eticheta("Selectie variabile:", stil=stil2), self.ch_selectie_variabile)
        layout_parametrii.addLayout(formLayout)
        layout_parametrii.addWidget(self.l_variabile_selectate)

        grup_model = qw.QGroupBox("Model")
        layout_model = qw.QVBoxLayout()
        layout_model.addWidget(self.b_actiune1)
        # Adaugare alte butoane
        # ...
        layout_model.setAlignment(Qt.AlignTop)
        grup_model.setLayout(layout_model)

        # Layoutul central
        layout_central = qw.QHBoxLayout()
        layout_central.addLayout(layout_parametrii)
        layout_central.addWidget(grup_model)

        panel_continut = gui.Panel(layout_central)

        self.form = gui.Frame(panel=panel_continut, titlu="Aplicatie sablon")

    def citire_fisier(self):
        dialog = qw.QFileDialog(directory=".")
        dialog.setFileMode(qw.QFileDialog.AnyFile)
        dialog.setNameFilter("Fisier date (*.csv)")
        dialog.setViewMode(qw.QFileDialog.Detail)
        fileNames = []
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
        if len(fileNames) == 0:
            return
        self.fisier = fileNames[0]
        self.tabel_date = pd.read_csv(self.fisier)
        variabile = list(self.tabel_date)
        self.l_variabile_selectate.clear()
        self.c_variabila_index.clear()
        for v in variabile:
            # Se instantiaza un item si se indica prin parametru lista la care va fi adaugat
            item = qw.QListWidgetItem(self.l_variabile_selectate)
            ch = qw.QCheckBox(v)
            # Inregistrare semnal de schimbare stare
            ch.stateChanged.connect(self.selectie_variabila)
            self.l_variabile_selectate.setItemWidget(item, ch)
            self.c_variabila_index.addItem(v)

    def selectie_variabila(self):
        self.date_citite = False
        for i in range(self.l_variabile_selectate.count()):
            item = self.l_variabile_selectate.item(i)
            ch_variabila = self.l_variabile_selectate.itemWidget(item)

    def selectie_toate_variabilele(self):
        flag = self.ch_selectie_variabile.isChecked()
        for i in range(self.l_variabile_selectate.count()):
            item = self.l_variabile_selectate.item(i)
            self.l_variabile_selectate.itemWidget(item).setChecked(flag)
        self.date_citite = False

    def citire_date(self):
        self.variabile_selectate.clear()
        for i in range(self.l_variabile_selectate.count()):
            item = self.l_variabile_selectate.item(i)
            checkItem = self.l_variabile_selectate.itemWidget(item)
            if checkItem.isChecked():
                self.variabile_selectate.append(checkItem.text())
        self.coloana_index = self.c_variabila_index.currentText()
        self.tabel_date.index = [str(v) for v in self.tabel_date[self.coloana_index]]
        self.nume_instante = self.tabel_date[self.coloana_index]
        self.date_citite = True

    def alerta(self, mesaj):
        msgBox = qw.QMessageBox()
        msgBox.setText(mesaj)
        msgBox.exec()

    def actiune1(self):
        if self.tabel_date is None:
            self.alerta("Nu au fost citite datele!")
            return
        if not self.date_citite:
            self.citire_date()
        print(self.tabel_date[self.variabile_selectate].values)
