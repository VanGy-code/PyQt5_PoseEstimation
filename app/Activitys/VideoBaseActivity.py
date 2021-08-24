#  ____                 ___       __                          
# /\  _`\           __ /\_ \     /\ \  __                     
# \ \ \L\ \  __  __/\_\\//\ \    \_\ \/\_\    ___      __     
#  \ \  _ <'/\ \/\ \/\ \ \ \ \   /'_` \/\ \ /' _ `\  /'_ `\   
#   \ \ \L\ \ \ \_\ \ \ \ \_\ \_/\ \L\ \ \ \/\ \/\ \/\ \L\ \  
#    \ \____/\ \____/\ \_\/\____\ \___,_\ \_\ \_\ \_\ \____ \ 
#     \/___/  \/___/  \/_/\/____/\/__,_ /\/_/\/_/\/_/\/___L\ \
#                                                      /\____/
#                                                      \_/__/  
from PIL import Image

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from config import font_style

import numpy as np 
import cv2
import mediapipe as mp


class VideoBaseActivity(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info_widgets = QWidget()
        self.info_layout = QHBoxLayout()
        self.info_widgets.setLayout(self.info_layout)
        self.info_layout.setAlignment(Qt.AlignLeft)

        self.score_label = QLabel('Score: ')
        self.score_label.setFont(QFont(QFont(font_style, 24, 75)))
        self.score_label.setAlignment(Qt.AlignBottom)
        self.score_label.setFixedWidth(120)
        # TODO：实时分数更新
        self.score_text = QLabel('092.64')
        self.score_text.setFont(QFont(QFont(font_style, 20, 60)))
        self.score_text.setAlignment(Qt.AlignBottom)

        self.line_0 = QFrame()
        self.line_0.setFrameShape(QFrame.VLine)
        self.line_0.setFrameShadow(QFrame.Sunken)
        self.line_0.setObjectName("line")

        self.action_label = QLabel("Action: ")
        # TODO：实时更新识别的动作
        self.recg_label = QLabel('正手高远球')
        self.action_label.setFont(QFont(QFont(font_style, 24, 75)))
        self.action_label.setAlignment(Qt.AlignBottom)
        self.action_label.setFixedWidth(120)
        self.recg_label.setFont(QFont(QFont(font_style, 20, 50)))
        self.recg_label.setAlignment(Qt.AlignBottom)
        

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.player_container = QWidget()
        self.player_container_layout = QVBoxLayout()
        self.player_container.setLayout(self.player_container_layout)

        self.media_container = QWidget()
        self.media_container_layout = QHBoxLayout()
        self.media_container.setLayout(self.media_container_layout)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

        # 屏幕画面对象
        self.cap = cv2.VideoCapture('')
        # self.cap.set(3,350)
        # self.cap.set(4,700)
        self.cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        # 定时器
        self.timer_video = QTimer()
        

        # TODO: 原视频显示窗口
        self.origin_video_layout = QHBoxLayout()
        self.origin_video = QWidget()
        self.origin_video_layout.setSpacing(0)
        self.origin_video.setLayout(self.origin_video_layout)
        self.original_video_label = QLabel('')
        self.origin_video_layout.addWidget(self.original_video_label)

        self.original_video_label.setFixedWidth(50)
        self.original_video_label.setFixedHeight(50)
        self.origin_video.setFixedWidth(350)
        self.origin_video.setFixedHeight(500)
        

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        # TODO: 识别视频显示窗口
        self.processed_video_layout = QHBoxLayout()
        self.processed_video = QWidget()
        self.processed_video_layout.setSpacing(0)
        self.processed_video.setLayout(self.processed_video_layout)
        self.processed_video_label = QLabel('')
        self.processed_video_layout.addWidget(self.processed_video_label)

        self.processed_video_label.setFixedHeight(50)
        self.processed_video_label.setFixedWidth(50)
        self.processed_video.setFixedWidth(350) 
        self.processed_video.setFixedHeight(500)

        # 进度条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        # TODO: 设置最大值
        self.slider.setMaximum(100)
        # TODO: 步长
        self.slider.setSingleStep(1)
        # TODO: 设置当前值
        self.slider.setValue(20)
        # TODO: 刻度位置，刻度下方
        self.slider.setTickPosition(QSlider.TicksBelow)

        # 播放、暂停按钮
        # TODO: 快进、快退、倍速
        self.control_widget = QWidget()
        self.control_layout = QHBoxLayout()
        self.control_widget.setLayout(self.control_layout)

        self.play_icon = QIcon('./source/image/play-light.png')
        self.pause_icon = QIcon('./source/image/pause-light.png')
        self.play_signal = False
        self.play_pause_button = QPushButton('')

        self.init_ui()
    
    def init_ui(self):
        self.info_layout.addWidget(self.score_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.score_text, Qt.AlignBottom)
        self.info_layout.addWidget(self.line_0)
        self.info_layout.addWidget(self.action_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.recg_label,Qt.AlignBottom)

        self.media_container_layout.addWidget(self.origin_video)
        self.media_container_layout.addWidget(self.line)
        self.media_container_layout.addWidget(self.processed_video)

        self.set_default_image(self.original_video_label)
        self.set_default_image(self.processed_video_label)

        self.play_pause_button.clicked.connect(self.change_video_status)

        self.play_pause_button.setIcon(self.play_icon)
        self.control_layout.addStretch(6)
        self.control_layout.addWidget(self.play_pause_button)
        self.control_layout.addStretch(6)
        
        self.player_container_layout.addWidget(self.media_container)
        self.player_container_layout.addWidget(self.slider)
        self.player_container_layout.addWidget(self.control_widget)

        self.layout.addWidget(self.info_widgets)
        self.layout.addWidget(self.player_container)

    def slotStart(self):
        self.timer_video.timeout.connect(self.show_video)
        self.timer_video.start(40)

    def set_default_image(self, label):
        image = QPixmap('./source/image/pic_none.png')
        # image.load(image_path)
        label.setPixmap(image)
        label.setScaledContents(True)

    def setVideo(self):
        video_file,_ = QFileDialog.getOpenFileName(self, "请选择视频所在路径", './data')
        self.cap = cv2.VideoCapture(video_file)

        self.slotStart()
        self.original_video_label.setFixedWidth(350)
        self.original_video_label.setFixedHeight(500)
        
        self.processed_video_label.setFixedWidth(350)
        self.processed_video_label.setFixedHeight(500)
        

    def show_video(self):
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame,1)
            frame = self.crop_image(frame, 360, 360)
            original_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            show_original_frame = QImage(original_frame.data, original_frame.shape[1],original_frame.shape[0],QImage.Format_RGB888)
            # 显示原相机图像
            self.original_video_label.setPixmap(QPixmap.fromImage(show_original_frame))

            show_processed_frame = self.process_frame(original_frame)
            # 处理后的图像
            self.processed_video_label.setPixmap(QPixmap.fromImage(show_processed_frame))
        else:
            self.cap.release()
            self.timer_video.stop()

    def process_frame(self, frame, with_canvas=False):

        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.pose.process(frame)

        if with_canvas == True:
            canvas = np.zeros([500, 500, 3], np.uint8) + 255

        if results.pose_landmarks:
            # draw img
            if with_canvas == True:
                self.mp_drawing.draw_landmarks(canvas, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                frame = QImage(frame.data, frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                canvas = QImage(canvas.data, canvas.shape[1],canvas.shape[0],QImage.Format_RGB888)
                return frame, canvas
            else:
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                frame = QImage(frame.data, frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                return frame

    def crop_image(self, re_img, new_height, new_width):
        re_img=Image.fromarray(np.uint8(re_img))
        width, height = re_img.size
        left = (width - new_width)/2
        top = (height - new_height)/2
        right = (width + new_width)/2
        bottom = (height + new_height)/2
        crop_im = re_img.crop((left, top, right, bottom)) #Cropping Image
        crop_im = np.asarray(crop_im)
        return crop_im

    # TODO: 
    def change_video_status(self):
        if self.play_signal is False:
            # TODO: 发送视频播放信号 
            self.play_pause_button.setIcon(self.pause_icon)
            self.play_signal = True
        else:
            # TODO: 发送视频暂停信号
            self.play_pause_button.setIcon(self.play_icon)
            self.play_signal = False