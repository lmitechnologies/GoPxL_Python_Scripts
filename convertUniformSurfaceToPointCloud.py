#created December 17 2024
#written by Bobby Breyer
#number of inputs 1
#Uniform Surface

#This tool takes a uniform surface and converts it to a surface point cloud


import numpy as np

#convert uniform surface to non-uniform surface
surface = get_surface(0)

xRes = surface.scale.x
yRes = surface.scale.y
zRes = surface.scale.z
xOff = surface.offset.x
yOff = surface.offset.y
zOff = surface.offset.z
length = surface.points.shape[0]
width = surface.points.shape[1]
size = width*length

Xarr = np.asarray(range(width),dtype=np.int16)
Xarr = np.tile(Xarr, length)
Yarr = np.arange(length,dtype=np.int16)
Yarr = np.repeat(Yarr, repeats=width)
Z = surface.points.copy()
Zarr = Z
Zarr = Zarr.flatten()

data_3DXYZ = np.stack((Xarr,Yarr,Zarr), axis = 1)
reshaped_array = data_3DXYZ.reshape(length, width, 3)

send_surface(0, surface.offset, surface.scale, reshaped_array)

#number of outputs 1
#Surface Point Cloud
