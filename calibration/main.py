import cv2 as cv
import numpy as np
import pyzed.sl as sl

def create_calibration_image(_height, _width):
    #img = (np.zeros((_height, _width, 3)) * 255).astype(np.uint8)
    img = (np.ones((_height, _width, 3)) * 255).astype(np.uint8)
    size = 10
    #top_left_corner = ((int (img.shape[1]/2 - size), int (img.shape[0]/2 - size)))
    #bottom_right_corner = ((int (img.shape[1]/2 + size), int (img.shape[0]/2 + size)))
    top_left_corner = (610, 325)
    bottom_right_corner = (675, 400)
    #print(top_left_corner)
    #print(bottom_right_corner)
    cv.rectangle(img, top_left_corner, bottom_right_corner, (0,0, 255), 2)
    return img

def start_stream():
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.QUALITY  # https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1DEPTH__MODE.html
    init_params.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
    init_params.depth_minimum_distance = 0.4
    init_params.depth_maximum_distance = 1.0
    init_params.camera_resolution = sl.RESOLUTION.HD2K
    init_params.enable_image_enhancement = False

    zed = sl.Camera()
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(err)
        exit(-1)
    return zed


if __name__=="__main__":
    height = 720
    width = 1280
    cam = start_stream()
    calib_img = create_calibration_image(_height = height, _width = width)
    runtime_parameters = sl.RuntimeParameters() # Create and set RuntimeParameters after opening the camera
    runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL # STANDARD 50 CONFIDENCE THRESHOLD, FILL 100 CONFIDENCE THRESHOLD
    image = sl.Mat()
    alpha = 0.5
    beta = 1 - alpha

    while True:
        if cam.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(image, sl.VIEW.LEFT)
            img_cv = (image.get_data())[:,:,:3]
            img_cv = cv.resize(img_cv, (width, height))
            #combined_img = cv.addWeighted(img_cv, alpha, calib_img, beta, 0.0)
            combined_img = cv.addWeighted(calib_img, alpha, img_cv, beta, 0.0)
            cv.imshow("zed", combined_img) 
            if cv.waitKey(1) == ord('q'):
                break
    cam.close() 
