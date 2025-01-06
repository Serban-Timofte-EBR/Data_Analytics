import sys
import PySide2.QtWidgets as qw
import model

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    frame = model.model_class()
    frame.form.show()
    sys.exit(app.exec_())
