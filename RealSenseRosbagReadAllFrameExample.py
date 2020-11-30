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



def write_csv(depth_frame,frame_no,filename):

    
    output_folder = filename+"_output"
    
 
    # current_directory = os.getcwd()
    # final_directory = os.path.join(current_directory, output_folder)
    os.makedirs(output_folder, exist_ok=True)

    print ( "writing depth data frame " +str(frame_no))
    f = open(output_folder+"/"+filename+"_depthdata"+str(frame_no)+".csv", "w")
    for y in range(480):
        for x in range(640):
            dist=depth_frame.get_distance(x,y)
            f.write( str(x+1) + "," +str(y+1)+","+str(dist)+"\n") # i added 1 to because pixel 0,0 does not make sense outside of this program
            
    f.close()



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
    rs.config.enable_device_from_file(config, args.input)
    print("Reading from bag file " + args.input)
    filename = ntpath.basename(args.input)
    filename = os. path. splitext(filename)[0]
    print (filename)
    # Configure the pipeline to stream the depth stream
    #config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    print("config")
    # Start streaming from file
    profile = pipeline.start(config)
    playback = profile.get_device().as_playback()
    playback.set_real_time(False)
    print("pipeline start")
    
    loop = 0
    previous_frame_no= 0
    frame_no= 0
    # Streaming loop
    while True:
        loop += 1
        #Somehow if not paused will cause the playback to loop the first 32 frames
        if loop % 20 == 0:
            playback.pause()
            playback.resume()
        # print(loop)
        # Get frameset of depth
        #print("pstart")
        
        frames = pipeline.wait_for_frames()
        
        # while not frames :
            # playback.resume()
            # time.sleep(0.005)
            # frames = pipeline.poll_for_frames()
            # playback.pause()
        
        #print("ppause")
        # frames = pipeline.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()
        
        #set frame no checking
        previous_frame_no = frame_no
        frame_no = depth_frame.get_frame_number()
        
        #break if looping the recording
        # if not depth_frame: continue
        # print(previous_frame_no, end="")
        # print(frame_no)
        if frame_no < previous_frame_no: break
        
        print("Getting frame" + str(frame_no))
        frame_dict[frame_no] = depth_frame
        
except Exception as ex:
    print(ex)
finally:
    
    print("Total acquired frames:", end='')
    print(len(frame_dict))
    
    dict_keys= list(frame_dict.keys())
    print("Frame range from:", end='')
    print(dict_keys[0], end='')
    print(" to ", end='')
    print(dict_keys[-1])
    
    for dframe_no, ddepth_frame in frame_dict.items() :
        write_csv(ddepth_frame,dframe_no,filename)
    print("finished")
    
    pass
