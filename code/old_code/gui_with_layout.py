import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


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


class ImgViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        self.label = QLabel(self)
        pixmap = QPixmap('../image.jpg')
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        #self.label.mousePressEvent = self.getPosition
        #self.show()

    def getPosition(self, event):
        width = event.pos().x()
        height = event.pos().y()
        print(width, height)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")

        """
        v_layout = QVBoxLayout()
        v_layout.addWidget(Color('red'))
        v_layout.addWidget(Color('green'))
        v_layout.addWidget(Color('blue'))
        h_layout = QHBoxLayout()
        h_layout.addWidget(Color('yellow'))
        h_layout.addWidget(Color('orange'))
        v_layout.addLayout(h_layout)
        """
        self.annotationWindow = AnnotationWindow()
        self.imageViewer = ImgViewer()
        self.imageViewer.label.mousePressEvent = self.allowAnnotation()
        self.annotationWindow.buttonOK.setEnabled(False)

        stack_left = QHBoxLayout()
        stack_left.addWidget(self.imageViewer)
        
        stack_right = QVBoxLayout()
        stack_right.addWidget(self.annotationWindow)
        stack_right.addWidget(Color("blue"))
        
        stack_left.addLayout(stack_right)

        widget = QWidget()
        widget.setLayout(stack_left)
        self.setCentralWidget(widget)
    
    def allowAnnotation(self):
        print()
        self.annotationWindow.buttonOK.setEnabled(True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()