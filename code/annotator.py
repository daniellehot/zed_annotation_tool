import cv2 as cv
import os
import time
import tkinter_gui as gui
import csv

FOLDER_PATH = "data/new/"
COLOR = (0, 0, 255)

class ImageViewer():
    def __init__(self, path):
        self.imgPath = path + ".png"
        self.annotationFile = path + "_a.csv"
        self.mode = "annotating"
        self.scaledImg = None
        self.fullSizedImg = None
        self.guiInstance = None
        self.annotationsDone = False
        self.coordinates = []
        self.species = []
        self.ids = []
        self.loadImage()

    
    def loadImage(self):
        self.fullSizedImg = cv.imread(self.imgPath)
        self.scaledImg = cv.resize(self.fullSizedImg, (1280, 720))

    
    def annotate(self):    
        cv.namedWindow("annotation window")
        cv.setMouseCallback("annotation window", self.draw)
        
        while 1:     
            cv.imshow("annotation window", self.scaledImg)
            k = cv.waitKey(20) & 0xFF
            if k == 27: #ESC
                if len(self.coordinates) != 0:
                    formattedAnnotations = self.formatAnnotations()
                    self.saveAnnotations(formattedAnnotations)
                    self.reset()
                    self.annotationsDone = True
                    break
                else:
                    print("Annotate the image")
            if k == ord('m'):
                if self.mode == "annotating":
                    self.mode = "MODE CORRECTING"
                    print(self.mode)
                    cv.setMouseCallback("annotation window", self.remove)
                else:
                    self.refreshImage()
                    self.mode = "MODE ANNOTATING"
                    print(self.mode)
                    cv.setMouseCallback("annotation window", self.draw)
        cv.destroyAllWindows()

    
    def draw(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            coordinate = (x,y)
            id, species = self.get_annotation()
            annotation = id + species
            if species != "cancel":
                cv.circle(self.scaledImg, coordinate, 5, COLOR, -1)
                cv.putText(self.scaledImg, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2, cv.LINE_AA, False)
                self.coordinates.append(coordinate)
                self.species.append(species)
                self.ids.append(id)

    #TODO Different distance function
    def remove(self, event, x, y, flags, param):    
        if event == cv.EVENT_LBUTTONDOWN:
            for coordinate in self.coordinates:
                sum = abs(x-coordinate[0] + y-coordinate[1])
                if sum < 10:
                    idx =self.coordinates.index(coordinate)
                    cv.drawMarker(self.scaledImg, self.coordinates[idx], COLOR, cv.MARKER_TILTED_CROSS, 50, 2)
                    self.coordinates.pop(idx)
                    self.species.pop(idx)
                    self.ids.pop(idx)
                    break


    def get_annotation(self):
        self.guiInstance = gui.AnnotationApp()
        while True:
            self.guiInstance.master.update()
            if self.guiInstance.cancelled:
                print("Annotation cancelled")
                self.guiInstance.master.destroy()
                self.guiInstance = None
                return  str(-1), "cancel"
            if self.guiInstance.id != -1 and self.guiInstance.species != None:
                print("Annotation acquired")
                id = self.guiInstance.id
                species = self.guiInstance.species
                self.guiInstance.master.destroy()
                self.guiInstance = None
                return id, species

    
    def refreshImage(self):
        self.scaledImg = cv.resize(self.fullSizedImg, (1280, 720))
        for (coordinate, species, id) in zip(self.coordinates, self.species, self.ids):
            cv.circle(self.scaledImg, coordinate, 5, COLOR, -1)
            annotation = id + species
            cv.putText(self.scaledImg, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, COLOR, 2, cv.LINE_AA, False)


    def formatAnnotations(self):
        scale_width = self.fullSizedImg.shape[1]/self.scaledImg.shape[1]
        scale_height = self.fullSizedImg.shape[0]/self.scaledImg.shape[0]
        data_formated = []
        for (species, id, xy) in zip(self.species, self.ids, self.coordinates):
            data_formated.append([species, id, int(xy[0]*scale_width), int(xy[1]*scale_height) ])
        return data_formated


    def saveAnnotations(self, data):
        with open(self.annotationFile, 'a') as f: 
            writer = csv.writer(f)
            header = ['species', 'id', 'x', 'y'] 
            writer.writerow(header)
            for annotation in data:
                writer.writerow(annotation) 


    def reset(self):
        self.coordinates.clear()
        self.species.clear()
        self.ids.clear()


def scan_for_new_files(path):
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            return filename.replace(".png", "")


if __name__=="__main__":
    lastAnnotatedFile = None
    while True:
        file = scan_for_new_files(FOLDER_PATH)
        if file != None and file != lastAnnotatedFile:
            imgViewer = ImageViewer(FOLDER_PATH + file)
            imgViewer.annotate()
            if imgViewer.annotationsDone:
                lastAnnotatedFile = file
        else:
            print("No new image")
            time.sleep(1)
            
