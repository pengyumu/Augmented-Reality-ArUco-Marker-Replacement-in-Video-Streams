# -*- coding: utf-8 -*-
"""place virtual object.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LlFLNz30NMc7Njjy-WrXh_d8XhhmL7wW
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Predefined dictionary lookup for ArUco markers
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()

# Read the video
cap = cv2.VideoCapture('aruco.mp4')

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for mp4 files
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

# Load the image patches for each ArUco marker
image_patches = {
    0: cv2.imread('patch_0.png'),
    1: cv2.imread('patch_1.png'),
    2: cv2.imread('patch_2.png'),
    3: cv2.imread('patch_3.png')
}

# Debug: Check if image patches are loaded correctly
for i, patch in image_patches.items():
    if patch is None:
        print(f"Error: Image patch for ID {i} not loaded correctly.")

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Video stream or file could not be opened or found.")

# Read until video is completed
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Debug: Print out to confirm the loop is running
        print("Reading a frame from the video...")

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the markers in the image
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)

        if ids is not None:
            # Debug: Print detected marker IDs
            print(f"Detected marker IDs: {ids}")

            for corner, id in zip(corners, ids.flatten()):
                if id in image_patches:
                    # Resize the replacement image to the size of the marker
                    marker_size_in_pixels = int(cv2.norm(corner[0][0] - corner[0][1]))
                    replacement_img = cv2.resize(image_patches[id], (marker_size_in_pixels, marker_size_in_pixels))

                    # Calculate homography
                    pts_dst = corner[0].astype(np.float32)  # Destination points are the marker corners
                    pts_src = np.float32([[0, 0], [marker_size_in_pixels - 1, 0], [marker_size_in_pixels - 1, marker_size_in_pixels - 1], [0, marker_size_in_pixels - 1]])  # Source points are the corners of the replacement image

                    h, status = cv2.findHomography(pts_src, pts_dst)

                    # Warp the replacement image onto the marker in the frame
                    frame = cv2.warpPerspective(replacement_img, h, (frame.shape[1], frame.shape[0]), dst=frame, borderMode=cv2.BORDER_TRANSPARENT)
        else:
            # Debug: Print a message if no markers were detected
            print("No markers detected in this frame.")

        # Write the modified frame to the output video
        out.write(frame)

        # Display the resulting frame
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

        # Insert a short pause, required to display the images correctly within the notebook
        cv2.waitKey(25)
    else:
        print("No more frames to read or there was an error reading a frame.")
        break

# Release resources
cap.release()
out.release()

