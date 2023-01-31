import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Annotate'
        self.left = 500
        self.top = 500
        self.width = 240
        self.height = 210
        self.initUI()
        self.species = []
    
    def initUI(self):
        self.species = ["Cod", "Haddock", "Hake", "Horse mackerel", "Whiting", "Saithe", "Plaice", "Lemon sole", "Ling", "Lubbe", "Herring", "Mackerel"]
        print(self.species[4])
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.combobox = QComboBox(self)
        self.combobox.resize(200, 50)
        self.combobox.move(20, 20)
        self.combobox.addItems(self.species)
        self.combobox.setFont(QFont('Arial', 15))

        self.textbox = QLineEdit(self)
        self.textbox.setValidator(QIntValidator())
        self.textbox.resize(200, 50)
        self.textbox.setMaxLength(3)
        self.textbox.setFont(QFont('Arial', 15))
        self.textbox.move(20, 80)

        self.buttonOK = QPushButton("OK", self)
        self.buttonOK.resize(200, 50)
        self.buttonOK.move(20, 140)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())