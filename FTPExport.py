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