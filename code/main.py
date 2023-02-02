import cv2 as cv
import pyzed.sl as sl
import os
from pynput import keyboard
import numpy as np

## CONTROL FLAGS ##
FLAG_PREVIEW = 0
FLAG_SAVE = 0
FLAG_ANNOTATION = 0

## PATH CONSTANTS ##
RGB_PATH = "data/rgb/"
DEPTH_PATH = "data/depth/"
CONF_PATH = "data/confidence/"
PC_PATH = "data/pointclouds/"
INTRINSICS_PATH = "data/intrinsics/"
ANNOTATIONS_PATH = "data/annotations/"
NEW_PATH = "data/new/"
#CURRENT_IMG = None 


def create_folders():
    if not os.path.exists("data"):
        os.mkdir("data")
        os.mkdir(RGB_PATH)
        os.mkdir(DEPTH_PATH)
        os.mkdir(CONF_PATH)
        os.mkdir(PC_PATH)
        os.mkdir(INTRINSICS_PATH)
        os.mkdir(ANNOTATIONS_PATH)
        os.mkdir(NEW_PATH)


def on_press(key):
    global FLAG_PREVIEW, FLAG_SAVE, FLAG_ANNOTATION
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        #FLAG_KEY = key.char
        if (key.char == "s" and FLAG_PREVIEW == 1):
            FLAG_PREVIEW = 0
            FLAG_SAVE = 1
            FLAG_ANNOTATION = 0
    except AttributeError:
        print('special key {0} pressed'.format(key))


def start_stream():
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.QUALITY  # https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1DEPTH__MODE.html
    init_params.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
    init_params.depth_minimum_distance = 0.5
    init_params.depth_maximum_distance = 1.0
    init_params.camera_resolution = sl.RESOLUTION.HD2K

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(err)
        exit(-1)
    return zed


def get_filename(path):
    number_of_files = len(os.listdir(path))
    #print(number_of_files)
    number_of_files += 1
    number_of_files = str(number_of_files).zfill(5)
    return  number_of_files


def save_img(_img):
    filename = get_filename(RGB_PATH)
    path = NEW_PATH + filename + ".png"
    cv.imwrite(path, _img)
    print("Image saved")
    return filename


def save_depth(_map):
    filename = get_filename(DEPTH_PATH)
    path = NEW_PATH + filename + "_d.csv"
    np.savetxt(path, _map, delimiter=",")
    print("Depth map saved")


def save_confidence(_map):
    filename = get_filename(CONF_PATH)
    path = NEW_PATH + filename + "_c.csv"
    np.savetxt(path, _map, delimiter=",")
    print("Confidence map saved")


def save_pointcloud(_point_cloud):
    filename = get_filename(PC_PATH)
    path = NEW_PATH + filename + ".ply"
    _point_cloud.write(path)
    print("Pointcloud saved")


def save_intrinsics(_calibration_params):
    fx, fy = _calibration_params.fx, _calibration_params.fy
    cx, cy = _calibration_params.cx, _calibration_params.cy
    intrinsics = np.array([fx, fy, cx, cy], dtype=np.float32)
    filename = get_filename(INTRINSICS_PATH)
    path = NEW_PATH + filename + "_i.csv"
    np.savetxt(path, intrinsics, delimiter=",", header="fx, fy, cx, cy")
    print("Intrinsics saved")    


def move_files(_current):
    os.rename(NEW_PATH + _current + ".png", RGB_PATH + _current + ".png")
    os.rename(NEW_PATH + _current + "_d.csv", DEPTH_PATH + _current + ".csv")
    os.rename(NEW_PATH + _current + "_c.csv", CONF_PATH + _current + ".csv")
    os.rename(NEW_PATH + _current + ".ply", PC_PATH + _current + ".ply")
    os.rename(NEW_PATH + _current + "_i.csv", INTRINSICS_PATH + _current + ".csv")
    os.rename(NEW_PATH + _current + "_a.csv", ANNOTATIONS_PATH + _current + ".csv")

    
def checkIfNewFolderIsEmpty():
    if len(os.listdir(NEW_PATH)) != 0:
        return False
    else:
        return True


def main():
    global FLAG_PREVIEW, FLAG_SAVE, FLAG_ANNOTATION
    create_folders()
    
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    camera = start_stream()
    runtime_parameters = sl.RuntimeParameters() # Create and set RuntimeParameters after opening the camera
    runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL # STANDARD 50 CONFIDENCE THRESHOLD, FILL 100 CONFIDENCE THRESHOLD

    image = sl.Mat()
    depth = sl.Mat()
    confidence = sl.Mat()
    point_cloud = sl.Mat()

    FLAG_PREVIEW = 1
    FLAG_ANNOTATION = 0
    FLAG_SAVE = 0
    current = None
    try:
        while True:
             if camera.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                # Retrieve left image
                camera.retrieve_image(image, sl.VIEW.LEFT)
                img = (image.get_data())[:,:,:3] # Return RGB image + extra channel for memory type (I guess?)
                camera.retrieve_measure(depth, sl.MEASURE.DEPTH)
                depth_map = np.array(depth.get_data())
                camera.retrieve_measure(confidence, sl.MEASURE.CONFIDENCE)
                confidence_map = np.array(confidence.get_data())
                camera.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
                calibration_params = camera.get_camera_information().camera_configuration.calibration_parameters.left_cam
                
                if FLAG_PREVIEW: #show image    
                    scaled_img = cv.resize(img, (1280, 720))
                    cv.namedWindow('zed', cv.WINDOW_AUTOSIZE)
                    cv.imshow('zed', scaled_img)
                    cv.waitKey(1)
                
                if FLAG_SAVE:
                    cv.destroyWindow("zed")
                    if checkIfNewFolderIsEmpty():
                        current = save_img(img)
                        save_depth(depth_map)
                        save_confidence(confidence_map)
                        save_pointcloud(point_cloud)
                        save_intrinsics(calibration_params)
                        FLAG_PREVIEW = 0
                        FLAG_SAVE = 0
                        FLAG_ANNOTATION = 1
                        print("Waiting for annotation")
                    else:
                        FLAG_PREVIEW = 1
                        FLAG_SAVE = 0
                        FLAG_ANNOTATION = 0
                        print("Folder is not empty, something went wrong.")
                        
                if FLAG_ANNOTATION:
                    annotation_file = NEW_PATH + current + "_a.csv"
                    if os.path.exists(annotation_file):
                        move_files(current)
                        FLAG_PREVIEW = 1
                        FLAG_SAVE = 0
                        FLAG_ANNOTATION = 0
    except Exception as e: 
        print(e)
    finally:
        camera.close()
        exit(1)
    

if __name__=="__main__":
    main()