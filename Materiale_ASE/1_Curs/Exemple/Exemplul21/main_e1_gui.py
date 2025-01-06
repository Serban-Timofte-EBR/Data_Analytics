import sys
import PySide2.QtWidgets as qw
import PySide2.QtGui as qgui
import PySide2.QtCore as qc


def afisare():
    msg = qw.QMessageBox(qw.QMessageBox.Icon.Information, "Info", "Exemplul 1")
    msg.exec_()


def afisare2():
    print("Analiza in componente principale")


def afisare1():
    print("Analiza factoriala")


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    fereastra_aplicatie = qw.QMainWindow()
    buton = qw.QPushButton("Dati click")
    buton.setFixedSize(300, 50)
    buton.setFont(qgui.QFont("Times", 16, qgui.QFont.Bold))
    buton.clicked.connect(afisare)

    meniu = qw.QMenu("Analiza datelor")
    meniu.addAction("Analiza factoriala", afisare1)
    meniu.addAction("Analiza in componente principale", afisare2)

    fereastra_aplicatie.menuBar().addMenu(meniu)

    layout = qw.QVBoxLayout()
    layout.setAlignment(qc.Qt.AlignHCenter)
    layout.addWidget(buton)
    panel = qw.QWidget()
    panel.setLayout(layout)
    fereastra_aplicatie.setCentralWidget(panel)

    fereastra_aplicatie.setWindowTitle("Prima aplicatie")
    fereastra_aplicatie.setFixedSize(400, 100)
    fereastra_aplicatie.show()

    for widget in app.allWidgets():
        print("Componenta:", type(widget).__name__)
        print("Parinte:", type(widget.parentWidget()).__name__)
        print("Pozitie:", widget.pos().x(), widget.pos().y())
    app.exec_()
