#  ____                 ___       __                          
# /\  _`\           __ /\_ \     /\ \  __                     
# \ \ \L\ \  __  __/\_\\//\ \    \_\ \/\_\    ___      __     
#  \ \  _ <'/\ \/\ \/\ \ \ \ \   /'_` \/\ \ /' _ `\  /'_ `\   
#   \ \ \L\ \ \ \_\ \ \ \ \_\ \_/\ \L\ \ \ \/\ \/\ \/\ \L\ \  
#    \ \____/\ \____/\ \_\/\____\ \___,_\ \_\ \_\ \_\ \____ \ 
#     \/___/  \/___/  \/_/\/____/\/__,_ /\/_/\/_/\/_/\/___L\ \
#                                                      /\____/
#                                                      \_/__/  
import os
from PIL import Image
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

from app.Components.MVideoWidget import MVideoWidget

import cv2

from config import font_style

class CameraBaseActivity(QWidget):
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
        self.score_text = QLabel('000.00')
        self.score_text.setFont(QFont(QFont(font_style, 20, 60)))
        self.score_text.setAlignment(Qt.AlignBottom)

        self.line_0 = QFrame()
        self.line_0.setFrameShape(QFrame.VLine)
        self.line_0.setFrameShadow(QFrame.Sunken)
        self.line_0.setObjectName("line")

        self.action_label = QLabel("Action: ")
        # TODO：实时更新识别的动作
        self.recg_label = QLabel('Move')
        self.action_label.setFont(QFont(QFont(font_style, 24, 75)))
        self.action_label.setAlignment(Qt.AlignBottom)
        self.action_label.setFixedWidth(120)
        self.recg_label.setFont(QFont(QFont(font_style, 20, 50)))
        self.recg_label.setAlignment(Qt.AlignBottom)
        

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        self.window_widget = QWidget()
        self.window_layout = QVBoxLayout()
        self.window_widget.setLayout(self.window_layout)

        self.media_container = QWidget()
        self.media_container_layout = QHBoxLayout()
        self.media_container.setLayout(self.media_container_layout)

        # 屏幕画面对象
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,350)
        self.cap.set(4,700)
        self.cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
        # 定时器
        self.timer_camera = QTimer() 
        # 摄像头标号
        self.CAM_NUM = 0 

        # TODO: 使用多线程提高视频FPS

        # 原相机显示窗口
        self.origin_camera_output = QLabel('')
        self.origin_camera_output.setFixedWidth(350)
        self.origin_camera_output.setFixedHeight(700)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        # TODO: 相机动作识别显示窗口
        self.processed_camera_output = QLabel('')
        self.processed_camera_output.setFixedHeight(700)
        self.processed_camera_output.setFixedWidth(350)

        self.control_widget = QWidget()
        self.control_layout = QHBoxLayout()
        self.control_widget.setLayout(self.control_layout)

        self.camera_defeat_icon = QIcon('./source/image/camera.png')
        self.camera_on_icon = QIcon('./source/image/recording.png')
        self.camera_on_signal = False
        self.camera_button = QPushButton('')
        self.camera_button.setIcon(self.camera_defeat_icon)
        self.camera_button.setFixedWidth(40)
        self.camera_button.setStyleSheet('border-radius:15px;')

        self.init_ui()
        self.init_slot()
        self.update()
    
    def init_ui(self):
        
        self.info_layout.addWidget(self.score_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.score_text, Qt.AlignBottom)
        self.info_layout.addWidget(self.line_0)
        self.info_layout.addWidget(self.action_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.recg_label,Qt.AlignBottom)

        self.media_container_layout.addWidget(self.origin_camera_output)
        self.media_container_layout.addWidget(self.line)
        self.media_container_layout.addWidget(self.processed_camera_output)
        
        self.control_layout.addWidget(self.camera_button)

        self.window_layout.addWidget(self.media_container)
        self.window_layout.addWidget(self.control_widget)

        self.layout.addWidget(self.info_widgets)
        self.layout.addWidget(self.window_widget)

    def init_slot(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.camera_button.clicked.connect(self.change_camera_status)

    def change_camera_status(self):
        if self.camera_on_signal is False:
            # 发送视频播放信号 
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.Warning(self, u'Warning', u'Camera Not Find!',
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.camera_button.setIcon(self.camera_on_icon)
                self.camera_on_signal = True
        else:
            # 发送相机关闭信号
            self.timer_camera.stop()
            self.cap.release()
            self.origin_camera_output.clear()
            self.processed_camera_output.clear()
            self.camera_button.setIcon(self.camera_defeat_icon)
            self.camera_on_signal = False

    def show_camera(self):
        flag,self.image = self.cap.read()
        show = self.image
        show=cv2.flip(show,1)
        # show = cv2.resize(self.image,(300,700))
        show = self.crop_image(show, 800, 345)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        # 显示原相机图像
        self.origin_camera_output.setPixmap(QPixmap.fromImage(showImage))

        # TODO: 现实处理后的相机图像
        self.processed_camera_output.setPixmap(QPixmap.fromImage(showImage))

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
