#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
#import csv32 as csv
import ntpath
import time

import png
import threading




def write_csv(depth_frame,frame_no,filename,intr):

    
    output_folder = filename+"_output"
    
 
    # current_directory = os.getcwd()
    # final_directory = os.path.join(current_directory, output_folder)
    os.makedirs(output_folder, exist_ok=True)

    print ( "writing depth data frame " +str(frame_no))
    f = open(output_folder+"/"+filename+"_depthdata"+str(frame_no)+".csv", "w")
    for y in range(480):
        for x in range(640):
            object_coordinate = rs.rs2_deproject_pixel_to_point(intr, [x, y], depth_frame.get_distance(x, y))
            x_distance = object_coordinate[0]
            y_distance = object_coordinate[1]
            z_distance = object_coordinate[2] # this value is the same as depth
            # print('X: ' + str(x_distance) + ' Y: ' + str(y_distance) + ' Z: ' + str(z_distance))
            
            if z_distance > 0 :
                f.write( str(x_distance) + "," +str(y_distance)+","+str(z_distance)+"\n") # i added 1 to because pixel 0,0 does not make sense outside of this program
            
            # dist=depth_frame.get_distance(x,y)
            # f.write( str(x+1) + "," +str(y+1)+","+str(dist)+"\n") # i added 1 to because pixel 0,0 does not make sense outside of this program
            
    f.close()

def write_jpg(color_image,frame_no,filename):
    
    output_folder = filename+"_output"
    os.makedirs(output_folder, exist_ok=True)

    print ( "writing depth data frame " +str(frame_no))
    cv2.imwrite(output_folder + "/" + filename + "_color" + str(frame_no) + ".jpg", color_image) 


#f=open(r"D:\test_for_read\pyton_test\1.bag")
# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream resolution, fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input'
parser.add_argument("-i", "--input", type=str,help="Path to the bag file",default=r'C:\Users\wwanmarx\Documents\temp\Li\20201127_105259.bag')
#parser.add_argument('D:\test_for_read\pyton_test\1.bag')
#print(args.input)
# Parse the command line arguments to an object
args = parser.parse_args()


# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()


# ctx = rs.context();
# myplayback = ctx.load_device(args.input)
frame_dict = {}
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input,repeat_playback=False)
    
    #Getting filename
    print("Reading from bag file " + args.input)
    filename = ntpath.basename(args.input)
    filename = os. path. splitext(filename)[0]
    print (filename)
    
    # Configure the pipeline to stream the depth stream
    #config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    
    # Start streaming from file
    profile = pipeline.start(config)
    depthprofile = profile.get_stream(rs.stream.depth) 
    intr = depthprofile.as_video_stream_profile().get_intrinsics()
    playback = profile.get_device().as_playback()
    playback.set_real_time(False)
    print("pipeline start")
    
    
    frame_no= 0
    # Streaming loop
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        frame_no = color_frame.get_frame_number()
        print("Getting frame" + str(frame_no))
        frame_dict[frame_no]=""
        color_image = np.asanyarray(color_frame.get_data())
        
        # write_jpg(color_image,frame_no,filename)
        x = threading.Thread(target=write_jpg, args=(color_image,frame_no,filename))
        x.start()
        
        
except Exception as ex:
    print(ex)
finally:
    print(len(frame_dict),end='')
    print(" frame total")
    print("finished")
    
    pass
