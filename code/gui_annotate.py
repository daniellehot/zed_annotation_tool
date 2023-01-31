import gui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import time
import cv2 as cv
import csv 

FOLDER_PATH = "data/new/"
COORD, FISH, ID = [], [], [] #COORD is defined as an array of tuples (width, height)

def scan_for_new_files(path):
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            return filename.replace(".png", "")


def annotate(_img_path, _app):
    mode = "annotating"
    img = cv.imread(_img_path)
    img = cv.resize(img, (1280, 720))
    
    cv.namedWindow("annotation window")
    cv.setMouseCallback("annotation window", draw_point)
    
    while True:     
        cv.imshow("annotation window", img)
        k = cv.waitKey(20) & 0xFF
        if k == 27: #ESC
            break
        if k == ord('m'):
            if mode == "annotating":
                mode = "correcting"
                print(mode)
                cv.setMouseCallback("annotation window", remove_point)
            else:
                mode = "annotating"
                print(mode)
                cv.setMouseCallback("annotation window", draw_point)
    cv.destroyAllWindows()
    
    def draw_point(event, x, y, flags, param):
        nonlocal img, _app
        global COORD, FISH, ID
        if event == cv.EVENT_LBUTTONDOWN:
            coordinate = (x,y)
            color = (0, 0, 255) 
            ex = gui.AnnotationApp()
            _app.exec()
            species, id = ex.fish,ex.id
            annotation = id + species
            if species != "cancel":
                img = cv.circle(img, coordinate, 5, color, -1)
                img = cv.putText(img, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv.LINE_AA, False)
                COORD.append(coordinate)
                FISH.append(species)
                ID.append(id)


    def remove_point(event, x, y, flags, param):    
        nonlocal img
        global COORD, FISH, ID
        if event == cv.EVENT_LBUTTONDOWN:
            for coordinate in COORD:
                sum = abs(x-coordinate[0] + y-coordinate[1])
                if sum < 10:
                    idx = COORD.index(coordinate)
                    cv.drawMarker(img, COORD[idx], (0, 0, 255), cv.MARKER_TILTED_CROSS, 50, 2)
                    COORD.pop(idx)
                    FISH.pop(idx)
                    ID.pop(idx)
                    break


def confirm_annotation(img_path):
    img = cv.resize(img, (1280, 720))
    for (coordinate, species, id) in zip(COORD, fish, ID):
        img = cv.circle(img, coordinate, 5, (0, 0, 255), -1)
        annotation = id + species
        img = cv.putText(img, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA, False)
    cv.namedWindow("confirmation window")

    while 1:
        cv.imshow("confirmation window", img)
        cv.waitKey()
        #correct = input("Is this correct? Y/N \n")
        correct = messagebox.askyesno(" ", "Is this correct annotation?")
        if correct == True:
            cv.destroyAllWindows()
            return True
        elif correct == False:
            cv.destroyAllWindows()
            return False


if __name__=="__main__":
    previous_file = None

    while True:
        file = scan_for_new_files(FOLDER_PATH)
        if file != None and previous_file != file:
            annotation_file = FOLDER_PATH + file + ".csv"
            img_path = FOLDER_PATH + file + ".png"
            annotate(_img_path = img_path, _app = app)

            if confirm_annotation(img_path):
                data_formated = []
                for (fish, id, xy) in zip(FISH, ID, COORD):
                    data_formated.append([fish, id, int(xy[0]*SCALE_WIDTH), int(xy[1]*SCALE_HEIGHT) ])
                save_annotations(annotation_file, data_formated)
                previous_file = file
                reset()
            else:
                reset()
        else:
            time.sleep(2)
            continue
