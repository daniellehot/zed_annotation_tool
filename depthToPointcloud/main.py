import numpy as np
import cv2 as cv
import open3d as o3d

def deproject_point(_u, _v, _depth,_intrinsics):
    Xc = (_u - _intrinsics[2])*(_depth/_intrinsics[0])
    Yc = (_v - _intrinsics[3])*(_depth/_intrinsics[1])
    Zc = _depth
    return np.array([Xc, Yc, Zc])

def create_pointcloud(_points, _colors):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(_points)
    pcd.colors = o3d.utility.Vector3dVector(_colors)
    o3d.io.write_point_cloud("temp.ply", pcd, write_ascii=True)


if __name__=="__main__":
    bgr = cv.imread("../code/data/rgb/00004.png")
    rgb = cv.cvtColor(bgr, cv.COLOR_BGR2RGB) 
    print(rgb.shape)
    depth_map = np.genfromtxt("../code/data/depth/00004.csv", delimiter=",")
    print(depth_map.shape)
    conf_map = np.genfromtxt("../code/data/confidence/00004.csv", delimiter=",")
    print(conf_map.shape)
    intrinsics = np.genfromtxt("../code/data/intrinsics/00004.csv", delimiter=",") # fx, fy, cx, cy
    print(intrinsics)
    K = np.eye(3)
    K[0,0] = intrinsics[0]
    K[1,1] = intrinsics[1]
    K[0,2] = intrinsics[2]
    K[1,2] = intrinsics[3]


    depth_map_finite = np.nan_to_num(depth_map, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
    #print(depth_map_finite.shape)
    non_zero_indeces = depth_map_finite.nonzero()
    u = non_zero_indeces[1]
    #print(len(u))
    v = non_zero_indeces[0]
    #print(len(v))
    depth = depth_map_finite[v, u]
    color = rgb[v, u, :]
    #print(color.shape)
    #print(len(depth))
    #print(u, v, depth)

    points = deproject_point(_u=u, _v=v,  _depth=depth, _intrinsics=intrinsics)
    points = points.T
    #points = np.asarray(points)
    print(points.shape)
    create_pointcloud(_points=points, _colors=color)







