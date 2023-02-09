import cv2 as cv
import pyzed.sl as sl
import os
import math
from pynput import keyboard
import numpy as np
import tkinter_gui as gui
from tkinter import messagebox

class Viewer():
    def __init__(self):
        self.start_stream()
        self.start_keylistener()

        self.coordinates = []
        self.species = []
        self.ids = []
        self.saved = 0

        self.color = (0, 0, 255) #BGR
        self.mode = "annotating"

    def start_stream(self):
        init_params = sl.InitParameters()
        init_params.depth_mode = sl.DEPTH_MODE.QUALITY  # https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1DEPTH__MODE.html
        init_params.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
        init_params.depth_minimum_distance = 0.4
        init_params.depth_maximum_distance = 1.0
        init_params.camera_resolution = sl.RESOLUTION.HD2K
        init_params.enable_image_enhancement = False

        self.zed = sl.Camera()
        err = self.zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print(err)
            exit(-1)
        
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA,  5)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE,  30)
        self.zed.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, 12)
        
        self.runtime_parameters = sl.RuntimeParameters() # Create and set RuntimeParameters after opening the camera
        self.runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL # STANDARD 50 CONFIDENCE THRESHOLD, FILL 100 CONFIDENCE THRESHOLD

        self.image = sl.Mat()
        self.depth = sl.Mat()
        self.confidence = sl.Mat()
        self.point_cloud = sl.Mat()
        self.calibration_params = None
    
    def on_press(self, key):
        try:
            #print('alphanumeric key {0} pressed'.format(key.char))
            if key.char == "s" and len(self.coordinates) != 0:
                self.save_data()
                self.saved = 1
                self.color = (0, 255, 0)
            
            if key.char == "m":
                if self.mode == "annotating":
                    self.mode = "correcting"
                    self.color = (255, 0, 0)
                else:
                    self.mode = "annotating"
                    self.color = (0, 0, 255)
            
            if key.char == "r":
                self.coordinates.clear()
                self.species.clear()
                self.ids.clear()
                self.saved = 0
                self.mode = "annotating"
                self.color = (0, 0, 255)

            if key.char == "q":
                self.zed.close()
                cv.destroyAllWindows()
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def start_keylistener(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        keyboard_listener.start()

    def retrieve_measures(self):
        # Retrieve left image
        self.zed.retrieve_image(self.image, sl.VIEW.LEFT)
        self.img_cv = (self.image.get_data()) # Return RGB image + extra channel for memory type (I guess?)
        self.zed.retrieve_measure(self.depth, sl.MEASURE.DEPTH)
        self.depth_map = np.array(self.depth.get_data())
        self.zed.retrieve_measure(self.confidence, sl.MEASURE.CONFIDENCE)
        self.confidence_map = np.array(self.confidence.get_data())
        self.zed.retrieve_measure(self.point_cloud, sl.MEASURE.XYZRGBA)
        self.calibration_params = self.zed.get_camera_information().camera_configuration.calibration_parameters.left_cam

    def show(self):
        #window_title = "zed " + self.mode
        self.window_title = "zed"
        self.scaled_img = cv.resize(self.img_cv, (1280, 720))
        self.draw_annotations()
        cv.namedWindow(self.window_title, cv.WINDOW_AUTOSIZE)
        if self.saved:
            cv.setMouseCallback(self.window_title, self.popup)
        else:
            if self.mode == "annotating": 
                cv.setMouseCallback(self.window_title, self.draw)
            if self.mode == "correcting":
                cv.setMouseCallback(self.window_title, self.remove)  
        cv.imshow(self.window_title, self.scaled_img)

    def draw_annotations(self):
        for (coordinate, species, id) in zip(self.coordinates, self.species, self.ids):
            cv.circle(self.scaled_img, coordinate, 5, self.color, -1)
            annotation = id + species
            cv.putText(self.scaled_img, annotation, (coordinate[0]+5, coordinate[1]+5), cv.FONT_HERSHEY_SIMPLEX, 1, self.color, 2, cv.LINE_AA, False)

    def draw(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            coordinate = (x,y)
            id, species = self.get_annotation()
            annotation = id + species
            if species != "cancel":
                self.coordinates.append(coordinate)
                self.species.append(species)
                self.ids.append(id)

    def remove(self, event, x, y, flags, param):    
        if event == cv.EVENT_LBUTTONDOWN:
            for coordinate in self.coordinates:
                dist = math.sqrt(math.pow(x-coordinate[0], 2) + math.pow(y-coordinate[1],2))
                if dist < 10:
                    idx =self.coordinates.index(coordinate)
                    self.coordinates.pop(idx)
                    self.species.pop(idx)
                    self.ids.pop(idx)
                    break
    
    def popup(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            messagebox.showerror("Error", "Remove fish and reset by pressing 'r' key.")

    def get_annotation(self):
        self.guiInstance = gui.AnnotationApp()
        while True:
            self.guiInstance.master.update()
            if self.guiInstance.cancelled:
                #print("Annotation cancelled")
                self.guiInstance.master.destroy()
                self.guiInstance = None
                return  str(-1), "cancel"
            if self.guiInstance.id != -1 and self.guiInstance.species != None:
                #print("Annotation acquired")
                id = self.guiInstance.id
                species = self.guiInstance.species
                self.guiInstance.master.destroy()
                self.guiInstance = None
                return id, species

    def save_data(self):
        print("TODO")


if __name__=="__main__":
    viewer = Viewer()
    while True:
        if viewer.zed.grab(viewer.runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            viewer.retrieve_measures()
            viewer.show()
            cv.waitKey(1)
        else:   
            break