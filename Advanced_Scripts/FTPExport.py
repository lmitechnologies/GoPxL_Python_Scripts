#created April 23 2024
#written by Trevor Dally
#number of inputs 1
#Uniform Surface

#This tool takes a uniform surface, saves it as a PKL file
#then streams that file to an FTP server. 
#there needs to be post processing done to scale the
#data into engineering units. This script is at the bottom of this file.


import numpy as np
import pickle
import io
from ftplib import FTP
from datetime import datetime

import time

start = time.time()

surface = inputs.get_surface(0)

#generate meta data
metadata = {
    'xRes': surface.scale.x,
    'yRes': surface.scale.y,
    'zRes': surface.scale.z,
    'xOff': surface.offset.x,
    'yOff': surface.offset.y,
    'zOff': surface.offset.z,
    'length': surface.points.shape[0],
    'width': surface.points.shape[1],
    'size': surface.points.shape[0] * surface.points.shape[1]
}

# Store data and metadata in a dictionary
data_with_metadata = {'data': surface.points, 'metadata': metadata}
 
#generate local path
stamp = surface.header.stamp
frame = stamp.frame
now = datetime.now()
unique_filename = now.strftime("%Y-%m-%d_%H-%M-%S_Z_frameIndex_"+str(frame)+".pkl")

#Send file over FTP
# FTP server details
ftp_host = '127.0.0.1'
ftp_username = 'tester'
ftp_password = 'password'
remote_path = '/' + unique_filename  # The remote path where you want to upload the file

try:
    # Establish FTP connection and login
    if 'FTP' not in memory: 
        ftp = FTP(ftp_host)
        ftp.login(ftp_username, ftp_password)
        memory['FTP'] = ftp
        
    ftp = memory['FTP']
    
    data = pickle.dumps(data_with_metadata)
    data_stream = io.BytesIO(data)
    ftp.storbinary(f'STOR {remote_path}', data_stream)
except Exception as e:
    log_info(f"An error occurred: {e}")

send_measurement(0, time.time()-start)


#number of outputs 0
#no output needed


'''


#created April 15 2024
#written by Bobby Breyer
#number of inputs 1
#PKL file

#This script takes a PKL file
#then converts that data to a PCD file (point cloud)
#this script is meant to run on a PC instance of Python
#and not in GoPxL. 

import os
import pickle
import numpy as np
import open3d as o3d

pklFolder = pointToYourFTPFolder
for filename in os.listdir(pklFolder):
    if filename.endswith('.pkl'):
        # Load the pickled file
        file_path = os.path.join(pklFolder, filename)
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            # Extract metadata from the loaded dictionary
            loaded_metadata = data['metadata']
            pointCloudData = data['data']

            # Assign metadata values to variables
            xRes = loaded_metadata.get('xRes', None)
            yRes = loaded_metadata.get('yRes', None)
            zRes = loaded_metadata.get('zRes', None)
            xOff = loaded_metadata.get('xOff', None)
            yOff = loaded_metadata.get('yOff', None)
            zOff = loaded_metadata.get('zOff', None)
            length = loaded_metadata.get('length', None)
            width = loaded_metadata.get('width', None)
            size = loaded_metadata.get('size', None)

            #generate X array
            Xarr = (np.asarray(range(width), dtype=np.double) * xRes) + xOff
            Xarr = np.tile(Xarr, length)

            #generate Y array
            Yarr = (np.arange(length, dtype=np.double)* yRes) + yOff
            Yarr = np.repeat(Yarr, repeats=width)

            #flatten and generate Z array
            Z = pointCloudData.copy()
            Z = Z.astype(np.double)
            Z.setflags(write=1)
            Z[Z==-32768] = np.nan    
            Zarr = Z
            Zarr = Zarr.flatten()
            Zarr = (Zarr * zRes) + zOff   
            Zarr = np.round(Zarr, 10)

            #stack arrays
            data_3DXYZ = np.stack((Xarr,Yarr,Zarr), axis = 1)
            
            # Find the indices where Z is not NaN
            valid_indices = ~np.isnan(data_3DXYZ[:, 2])

            # Filter the data using boolean indexing
            filtered_data = data_3DXYZ[valid_indices]
            data_3DXYZ = data_3DXYZ.round()
            
            # Save point cloud in PCD format
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(data_3DXYZ)
            o3d.io.write_point_cloud(pklFolder +"\\" + filename + '.pcd', pcd, write_ascii=False)  # Set write_ascii=False for binary 
            print("Finished saving "+ filename)


#number of outputs 1
#saved PCD file


'''