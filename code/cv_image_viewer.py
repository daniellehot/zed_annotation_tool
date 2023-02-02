import cv2 as cv
import os
import time
import tkinter_gui as gui

FOLDER_PATH = "data/new/"

class ImageViewer():
    def __init__(self, path):
        self.imgPath = path + ".png"
        self.annotationFile = path + ".csv"
        self.mode = "annotating"
        self.scaledImg = None
        self.fullSizedImg = None
        self.guiInstance = None

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
                break
            if k == ord('m'):
                if self.mode == "annotating":
                    self.mode = "correcting"
                    print(self.mode)
                    cv.setMouseCallback("annotation window", self.remove)
                else:
                    self.mode = "annotating"
                    print(self.mode)
                    cv.setMouseCallback("annotation window", self.draw)
        cv.destroyAllWindows()

    
    def draw(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            #coordinate = (x,y)
            #self.scaledImg = cv.circle(self.scaledImg, coordinate, 5, (0, 0, 255), -1)
            coordinate = (x,y)
            colour = (0, 0, 255)
            id, species = self.get_annotation()
            annotation = id + species
            if species != "cancel":
                img = cv.circle(self.scaledImg, coordinate, 5, colour, -1)
                img = cv.putText(self.scaledImg, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, colour, 2, cv.LINE_AA, False)
                #self.rgb.append(colour)
                self.coordinates.append(coordinate)
                self.species.append(species)
                self.ids.append(id)


    def remove(self, event, x, y, flags, param):    
        if event == cv.EVENT_LBUTTONDOWN:
            for coordinate in self.coordinates:
                sum = abs(x-coordinate[0] + y-coordinate[1])
                if sum < 10:
                    idx =self.coordinates.index(coordinate)
                    cv.drawMarker(self.scaledImg, self.coordinates[idx], (0, 0, 255), cv.MARKER_TILTED_CROSS, 50, 2)
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
                #self.guiInstance.breakTheLoop = True 
                self.guiInstance = None
                return  str(-1), "cancel"
            if self.guiInstance.id != -1 and self.guiInstance.species != None:
                print("Annotation acquired")
                id = self.guiInstance.id
                species = self.guiInstance.species
                self.guiInstance.master.destroy()
                #self.guiInstance.breakTheLoop = True 
                self.guiInstance = None
                return id, species
            

def scan_for_new_files(path):
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            return filename.replace(".png", "")
        else:
            return None


if __name__=="__main__":
    while True:
        file = scan_for_new_files(FOLDER_PATH)
        if file != None:
            imgViewer = ImageViewer(FOLDER_PATH + file)
            imgViewer.annotate()
        else:
            print("No new image")
            time.sleep(1)
            
