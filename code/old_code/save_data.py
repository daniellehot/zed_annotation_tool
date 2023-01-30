########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import numpy as np
import open3d as o3d
import cv2 as cv


#https://www.stereolabs.com/docs/depth-sensing/depth-settings/

def get_pointcloud_value(pc, width, height):
    return pc.get_value(width, height)


def main():
    # Create a Camera object
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
        exit(1)


    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    # STANDARD 50 CONFIDENCE THRESHOLD, FILL 100 CONFIDENCE THRESHOLD
    runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL # https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1SENSING__MODE.html
    # Setting the depth confidence parameters
    #runtime_parameters.confidence_threshold = 100 #[1, 100]
    #runtime_parameters.texture_confidence_threshold = 100 #[1, 100]

    # Capture 150 images and depth, then stop
    image = sl.Mat()
    depth = sl.Mat()
    confidence = sl.Mat()
    normals = sl.Mat()
    point_cloud = sl.Mat()

    # A new image is available if grab() returns SUCCESS
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # Retrieve left image
        zed.retrieve_image(image, sl.VIEW.LEFT)
        img =(image.get_data())[:,:,:3] # Return RGB image + extra channel for memory type (I guess?)
        cv.imwrite("temp.png", img)
        print(img.shape)

        # Retrieve depth map. Depth is aligned on the left image
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
        depth_map = np.array(depth.get_data())
        print(depth_map.shape)
        np.savetxt("depth_map.csv", depth_map, delimiter=",")

        zed.retrieve_measure(confidence, sl.MEASURE.CONFIDENCE)
        confidence_map = np.array(confidence.get_data())
        print(confidence_map.shape)
        np.savetxt("confidence_map.csv", confidence_map, delimiter=",")

        # Retrieve colored point cloud. Point cloud is aligned on the left image.
        zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
        pc_np = np.array(point_cloud.get_data())
        point_cloud.write("temp.ply")

        #print(depth_map[600, 1000])
        #print(confidence_map[600, 1000])
        #print(pc_np[600, 1000, 2])
       
    zed.close()

if __name__ == "__main__":
    main()
