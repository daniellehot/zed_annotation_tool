import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AnnotationWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Annotation window
        self.AnnotationWindowTitle = 'Annotate'
        self.AnnotationWindowLeft = 500
        self.AnnotationWindowTop = 500
        self.AnnotationWindowWidth = 240
        self.AnnotationWindowHeight = 210
        self.initAnnotationUI()
        
        # Annotation variables 
        self.species = []
        self.id, self.fish = None, None

    def initAnnotationUI(self):
        self.species = ["cod", "haddock", "hake", "horse mackerel", "whiting", "saithe", "plaice", "lemon sole", "ling", "lubbe", "herring", "mackerel"]
        self.setWindowTitle(self.AnnotationWindowTitle)
        self.setGeometry(self.AnnotationWindowLeft, self.AnnotationWindowTop, self.AnnotationWindowWidth, self.AnnotationWindowHeight)

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
        self.buttonOK.clicked.connect(self.annotationWindow_onClick)
        #self.show()

    def annotationWindow_onClick(self):
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


    def closeEvent(self, event):
        print("I am closing the annotation widget")


# https://pyshine.com/Make-GUI-for-OpenCv-And-PyQt5/
# https://www.pythonguis.com/tutorials/creating-multiple-windows/
class ImgViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.annotationWindow = None

        self.coord = None
        self.COORDS = []
        self.IDS = []
        self.FISHES = []
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        self.label = QLabel(self)
        pixmap = QPixmap('../image.jpg')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.label.mousePressEvent = self.openAnnotationWindow
        self.show()

        print("temp")

    def getPosition(self, event):
        if self.annotationWindow is None:
            width = event.pos().x()
            height = event.pos().y()
            self.annotationWindow = AnnotationWindow()
            self.coord = (width, height)
            self.annotationWindow.show()
        else:
            print("COORDS ", self.COORDS)
            print("IDS ", self.IDS)
            print("FISHES ", self.FISHES)
            if self.annotationWindow.id is not None and self.annotationWindow.fish is not None:
                self.COORDS.append(self.coord)
                self.IDS.append(self.annotationWindow.id)
                self.FISHES.append(self.annotationWindow.fish)
                self.annotationWindow = None
                
    def openAnnotationWindow(self, event):
        if self.annotationWindow is None:
            self.annotationWindow = AnnotationWindow()
            self.annotationWindow.show()
            print(self.annotationWindow.id)
            print(self.annotationWindow.fish)
    


        


    def closeEvent(self, event):
        print("I am closing the image viewer")



if __name__=="__main__":
    app = QApplication(sys.argv)
    #ex1 = AnnotationApp()
    #annotationApp_inst = AnnotationApp()
    imgViewer = ImgViewer()
    app.exec()
    #sys.exit(app.exec_())   