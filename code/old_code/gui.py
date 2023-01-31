# TUTORIAL https://pythonpyqt.com/contents/
# https://pythonbasics.org/pyqt-buttons/
# https://pythonspot.com/pyqt5-textbox-example/

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def window():
   app = QApplication(sys.argv)
   widget = QWidget()
   
   button1 = QPushButton(widget)
   button1.setText("Cod")
   button1.move(64,32)
   button1.clicked.connect(button1_clicked)

   button2 = QPushButton(widget)
   button2.setText("Pollock")
   button2.move(64,64)
   button2.clicked.connect(button2_clicked)

   textbox = QLineEdit(widget)
   textbox.setValidator(QIntValidator())
   textbox.setMaxLength(3)
   textbox.move(64, 10)

   widget.setGeometry(50,50,320,200)
   widget.setWindowTitle("PyQt5 Button Click Example")
   widget.show()
   sys.exit(app.exec_())

def button1_clicked():
    print("Button 1 clicked")

def button2_clicked():
    print("Button 2 clicked")   


if __name__ == '__main__':
   window()

