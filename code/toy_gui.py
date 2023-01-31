import gui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import time
import cv2 as cv
import csv 


if __name__=="__main__":
    app = QApplication(sys.argv)
    ex = gui.AnnotationApp()
    app.exec()
    print(ex.id)
    print(ex.fish)
