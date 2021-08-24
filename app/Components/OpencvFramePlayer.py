#  __  __              __                ______              __      
# /\ \/\ \            /\ \              /\__  _\          __/\ \__   
# \ \ \ \ \    ___    \_\ \     __   _ _\/_/\ \/     ___ /\_\ \ ,_\  
#  \ \ \ \ \ /' _ `\  /'_` \  /'__`\/\`'__\\ \ \   /' _ `\/\ \ \ \/  
#   \ \ \_\ \/\ \/\ \/\ \L\ \/\  __/\ \ \/  \_\ \__/\ \/\ \ \ \ \ \_ 
#    \ \_____\ \_\ \_\ \___,_\ \____\\ \_\  /\_____\ \_\ \_\ \_\ \__\
#     \/_____/\/_/\/_/\/__,_ /\/____/ \/_/  \/_____/\/_/\/_/\/_/\/__/
                                                                   
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np 
import cv2
import mediapipe as mp

class OpenCVFramePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

        self.cap

    def init_ui(self):
        pass

    def process_image(self, frame):
        background = np.zeros([500, 500, 3], np.uint8) + 255

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            # draw img
            self.mp_drawing.draw_landmarks(background, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        return frame, background

    