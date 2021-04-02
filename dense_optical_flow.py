# -*- coding: utf-8 -*-
"""02_Dense_Optical_Flow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kuL5lJfcEci7T69aocZWTtn7KjlMnNkb
"""

# Import Libraries
import cv2 as cv
import numpy as np

# Video Capture
cap = cv.VideoCapture(0)

# Read the capture and get the first frame
ret, first_frame = cap.read()

# Convert frame to Grayscale
prev_gray = cv.cvtColor(first_frame,
                       cv.COLOR_BGR2GRAY)

# Create# Create an image with the same dimensions as the frame for later drawing purposes
mask = np.zeros_like(first_frame)

# Saturation to maximum
mask[..., 1] = 255

# While loop
while(cap.isOpened()):

    # Read the capture and get the first frame
    ret, frame = cap.read()
    
    # Open new window and display the input frame
    cv.imshow("Input", frame)
    
    # Convert all frame to Grayscale (previously we did only the first frame)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Calculate dense optical flow by Farneback
    flow = cv.calcOpticalFlowFarneback(prev_gray,
                                      gray,
                                      None,
                                      0.5,
                                      3,
                                      15,
                                      3,
                                      5,
                                      1.2,
                                      0)
    
    # Compute Magnitude and Angle
    magn, angle = cv.cartToPolar(flow[..., 0],
                                  flow[..., 1])
    
    # Set image hue depanding on the optical flow direction
    mask[..., 0] = angle*180/np.pi/2    
        
    # Normalize the magnitude
    mask[..., 2] = cv.normalize(magn,
                                None,
                                0,
                                255,
                                cv.NORM_MINMAX)
                                


    # Convert HSV to RGB
    rgb = cv.cvtColor(mask, cv.COLOR_HSV2RGB)
    
    # Open new window and display the output
    cv.imshow("Dense Optical Flow", rgb)
    
    # Update previous frame
    prev_gray=gray
    
    # Close the frame
    if cv.waitKey(30) & 0xff == ord('q'):
        break
    
# Release and Destroy
cap.release()
cv.destroyAllWindows()

