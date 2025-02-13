#created July 19 2024
#written by Torsten Huth
#number of inputs 1
#surface point cloud array

#This tool takes a point cloud and analyses intensity 
#it calculates min, max, average, median intensity
#and saves a histogram as png
#additional module: matplotlib needed 
#install matplot lib by: python3.exe -m pip install matplotlib (see also GoPxL manual)

# import numpy and matplotlib library
import numpy as np
import matplotlib.pyplot as plt

if any_input_invalid():
    send_all_invalid()
    
# import Profile/Surface data
data: SurfaceMsg = get_surface(0)

#intensity as array
intensity: np.array = data.intensity

#change data type to unsingned integer 8bit
intensity = intensity.astype(np.uint8)

#remove invalids
intensity = intensity[data.points != -32768]

# number of points from import data intensity with invalids
points_imported = np.array(data.intensity)
number_points_imported = points_imported.size

# number of points intensity after removing invalids
points_valid = np.array(intensity)
number_points_valid = points_valid.size

#calculate intensity values
average = np.mean(intensity)
median = np.median(intensity)
min = np.min(intensity)
max = np.max(intensity)

#HISTOGRAM

#define bins for intensity
#example use 8 fixed bins bin = (1, 33, 65, 97, 129, 161, 193, 225, 256) 
#bin= number of bins for intensity
bin=32

#histogram from intensity in bins, count intensity in bins
histbins, _ = np.histogram(intensity, bin)

#histogram from intensity in bins, normalized to 1
histbins_normalized, _ = np.histogram(intensity, bin, density=True)

#histogram from intensity in bins, normalized by number of valid points
histbins_valid_points, _ = np.histogram(intensity, bin)
histbins_valid_points = histbins_valid_points / number_points_valid

#plot histogram

#define scaling factor for percent
scale_percent = 100 / number_points_valid
#define array with size of valid points, filled with scaling factor for percent
array_scaling = [scale_percent]*number_points_valid
#labels for histogram
plt.title('Histogram', fontsize=20)
plt.xlabel('average:' +str(round(average, 1))+'      min:'+str(min)+'      max:'+str(max)+'                intensity', fontsize=10)
plt.ylabel('percent', fontsize=10)
#axis limits for plot histogram and add grid
#plt.ylim(0, 100)
plt.xlim(0, 300)
plt.grid()
#create histogram plot scaled by percent
plt.hist(intensity, bin, weights=array_scaling)
#save histogram plot as png and close plot (close needed, otherwise plot is cumulated)
plt.savefig(r'C:\GoTools\Script\measurement.png')
plt.close()


#output results
if is_valid(data):
    send_measurement(0, number_points_imported)
    send_measurement(1, number_points_valid)
    send_measurement(2, average)
    send_measurement(3, median)
    send_measurement(4, min)
    send_measurement(5, max)
    send_measurement(6, histbins)
    send_measurement(7, histbins_normalized*10000)
    send_measurement(8, histbins_valid_points*100)
else:
    send_measurement(0, 0)
    



#number of outputs 9
#output 0 measurement (number points loaded)
#output 1 measurement (number points valid)
#output 2 measurement (average intensity)
#output 3 measurement (median intensity)
#output 4 measurement (min intensity)
#output 5 measurement (max intensity)
#output 6 array (histogram count)
#output 7 array (histogram normalized to 1)
#output 8 array (histogram percent)
#output save histogram image as png (path C:\GoTools\Script\measurement.png)