from PySide2 import QtWidgets
import PySide2.QtWidgets as qw
from PySide2.QtCore import QAbstractTableModel, Qt


# Clasa pe post de container greu. Este extensie de QMainWindow care este container greu Qt
class Frame(qw.QMainWindow):
    # Constructor care primeste un panel de continut si titlul
    def __init__(self, panel, titlu):
        qw.QMainWindow.__init__(self)
        self.setWindowTitle(titlu)

        self.setCentralWidget(panel)

        # Dimensionare fereastra
        self.adjustSize()  # Pune dimensiunea in functie de continut


# Clasa care defineste un model de tabel
class ModelTabel(QAbstractTableModel):
    # Primeste un pandas DataFrame
    def __init__(self, data):
        super(ModelTabel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            coloana = index.column()
            linia = index.row()
            valoare = self._data.iloc[linia, coloana]
            return str(valoare)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data.columns)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


# Clasa de tip tabel
class Tabel(QtWidgets.QTableView):
    def __init__(self, data):
        QtWidgets.QTableView.__init__(self)
        self.horizontalHeader().setSectionResizeMode(
            qw.QHeaderView.ResizeToContents
        )
        self.verticalHeader().setSectionResizeMode(
            qw.QHeaderView.ResizeToContents
        )
        size = qw.QSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.setSizePolicy(size)
        self.setModel(ModelTabel(data=data))
        self.setFixedSize(700, 400)


class Panel(qw.QWidget):
    def __init__(self, gestionar_pozitionare):
        qw.QWidget.__init__(self)
        self.main_layout = gestionar_pozitionare
        self.setLayout(self.main_layout)


# Clasa generalizare buton
class Buton(qw.QPushButton):
    def __init__(self, text, w, h, stil=None, click=None):
        qw.QPushButton.__init__(self, text)
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        if stil is not None:
            self.setStyleSheet(stil)
        if click is not None:
            self.clicked.connect(click)


# Clasa generalizare eticheta
class Eticheta(qw.QLabel):
    def __init__(self, text, w=None, h=None, stil=None):
        qw.QLabel.__init__(self, text)
        if w is not None:
            self.setFixedWidth(w)
        if h is not None:
            self.setFixedHeight(h)
        if stil is not None:
            self.setStyleSheet(stil)


# Clasa generalizare text field
class TextField(qw.QLineEdit):
    def __init__(self, text, w=None, h=None, stil=None):
        qw.QLineEdit.__init__(self, text)
        if w is not None:
            self.setFixedWidth(w)
        if h is not None:
            self.setFixedHeight(h)
        if stil is not None:
            self.setStyleSheet(stil)
