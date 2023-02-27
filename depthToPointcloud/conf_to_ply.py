import numpy as np
import cv2 as cv
import open3d as o3d

def deproject_point(_u, _v, _depth, _intrinsics):
    Xc = (_u - _intrinsics[2])*(_depth/_intrinsics[0])
    Yc = (_v - _intrinsics[3])*(_depth/_intrinsics[1])
    Zc = _depth
    return np.array([Xc, Yc, Zc])

def create_pointcloud(_points, _colors, _conf):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(_points)
    pcd.colors = o3d.utility.Vector3dVector(_colors)
    filename = "temp_conf_"+str(_conf)+".ply"
    o3d.io.write_point_cloud(filename, pcd, write_ascii=True)

if __name__=="__main__":
    CONF_THRESHOLD = np.array([0, 25, 50, 75, 100])

    bgr = cv.imread("../code/data/rgb/00004.png")
    rgb = cv.cvtColor(bgr, cv.COLOR_BGR2RGB) 
    rgb_normalized = rgb/255
    print("RGB shape", rgb.shape)
    depth_map = np.genfromtxt("../code/data/depth/00004.csv", delimiter=",")
    print("DEPTH MAP shape", depth_map.shape)
    conf_map = np.genfromtxt("../code/data/confidence/00004.csv", delimiter=",")
    print("CONFIDENCE MAP shape", conf_map.shape)
    intrinsics = np.genfromtxt("../code/data/intrinsics/00004.csv", delimiter=",") # fx, fy, cx, cy
    print("INTRINSICS", intrinsics)

    for conf in CONF_THRESHOLD:
        depth_map_conf = np.where(conf_map > conf, depth_map, 0)
        print(depth_map_conf.shape)
        depth_map_finite = np.nan_to_num(depth_map_conf, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
        print(depth_map_finite.shape)
        non_zero_indeces = depth_map_finite.nonzero()
        u = non_zero_indeces[1]
        #print(len(u))
        v = non_zero_indeces[0]
        #print(len(v))
        depth = depth_map_finite[v, u]
        color = rgb_normalized[v, u, :]
        
        points = deproject_point(_u=u, _v=v,  _depth=depth, _intrinsics=intrinsics)
        points = points.T
        print(points.shape)
        create_pointcloud(_points=points, _colors=color, _conf=conf)







