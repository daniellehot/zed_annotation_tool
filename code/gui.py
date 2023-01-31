import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class AnnotationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Annotate'
        self.left = 500
        self.top = 500
        self.width = 240
        self.height = 210
        self.initUI()
        self.species = []
        self.id, self.fish = None, None
    
    def initUI(self):
        self.species = ["cod", "haddock", "hake", "horse mackerel", "whiting", "saithe", "plaice", "lemon sole", "ling", "lubbe", "herring", "mackerel"]
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
        self.buttonOK.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        id = self.textbox.text()
        if not id:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText("       Missing ID      ") #Keep the whitespace otherwise the message window is too small
            msg.setIcon(QMessageBox.Critical)
            msg.exec()
        else:
            self.id = id 
            self.fish = self.combobox.currentText() 
            self.close()


# https://pyshine.com/Make-GUI-for-OpenCv-And-PyQt5/
# https://www.pythonguis.com/tutorials/creating-multiple-windows/
class ImgViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.annotationWindow = None
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        self.label = QLabel(self)
        pixmap = QPixmap('../image.jpg')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.label.mousePressEvent = self.getPosition
        self.show()

    def getPosition(self, event):
        width = event.pos().x()
        height = event.pos().y()
        print(width, height)
        annWindow = AnnotationApp()


if __name__=="__main__":
    app = QApplication(sys.argv)
    #ex1 = AnnotationApp()
    imgViewer_inst = ImgViewer()
    app.exec()
    #sys.exit(app.exec_())   