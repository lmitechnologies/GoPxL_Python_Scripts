import numpy as np

if any_input_invalid():
    send_all_invalid()

surfaces = get_surface(0)
offsetArr = []
scaleArr = []
pointsArr = []

for surface in surfaces:
    #use unscaled units to save proc time
    heightLimitScaled = 25 #mm
    
    #formula for scaled to unscaled is (mm - offset)/res = unscaled
    zOffset = surface.offset.z
    zResolution = surface.scale.z
    heightLimitUnscaled = ((heightLimitScaled - zOffset)/zResolution)
    
    # Find indices where Z is below the unscaled threshold
    surfPts = surface.points.copy()
    indices = np.where(surfPts[:, :, 2] < heightLimitUnscaled)
    
    # Replace all corresponding X, Y, and Z values 
    surfPts[indices] = -32768 

    #setup output arrays
    offsetArr.append(surface.offset)
    scaleArr.append(surface.scale)
    pointsArr.append(surfPts)
    log_info("Done")

send_surface(0,offsetArr,scaleArr,pointsArr)


    