#created April 15 2024
#written by Bobby Breyer
#number of inputs 1
#Surface Point Cloud Array

#This tool takes a point cloud and removes data from below a threshold
#This can be useful when using a ring or wide align tool with unwanted 
#background data. Such data can't be masked out since no tool exists 
#(at the moment) to do so on non-uniform data. 

import numpy as np

if any_input_invalid():
    send_all_invalid()

surfaces = get_surface(0)
offsetArr = []
scaleArr = []
pointsArr = []

heightLimitScaled = 25 #threshold in mm

for surface in surfaces:
    
    #use unscaled data to process arrays faster
    #formula for scaled to unscaled is (mm - offset)/res = unscaled
    zOffset = surface.offset.z
    zResolution = surface.scale.z
    heightLimitUnscaled = ((heightLimitScaled - zOffset)/zResolution)
    
    # Find indices where Z is below the unscaled threshold
    surfPts = surface.points.copy()
    indices = np.where(surfPts[:, :, 2] < heightLimitUnscaled)
    
    # Replace all corresponding X, Y, and Z values with kNULL (-32768)
    surfPts[indices] = -32768 

    #setup output arrays
    offsetArr.append(surface.offset)
    scaleArr.append(surface.scale)
    pointsArr.append(surfPts)
    log_info("Done")

send_surface(0,offsetArr,scaleArr,pointsArr)


#number of outputs 1
#Surface Point Cloud Array    