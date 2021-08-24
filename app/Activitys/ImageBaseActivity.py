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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from config import font_style

class ImageBaseActivity(QWidget):

    local_file_import_signal = pyqtSignal()
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

        self.media_container = QWidget()
        self.media_container_layout = QHBoxLayout()
        self.media_container.setLayout(self.media_container_layout)

        # 原图片显示窗口
        self.image_container_1 = QWidget()
        self.image_container_1_layout = QHBoxLayout()
        self.image_container_1.setLayout(self.image_container_1_layout)

        self.origin_image_label = QLabel('')
        self.origin_image_label.setFixedWidth(50)
        self.origin_image_label.setFixedHeight(50)
        self.image_container_1.setFixedHeight(700)
        self.image_container_1.setFixedWidth(350)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        # TODO: 识别图片显示窗口
        self.image_container_2 = QWidget()
        self.image_container_2_layout = QHBoxLayout()
        self.image_container_2.setLayout(self.image_container_2_layout)

        self.processed_image_label= QLabel('')
        self.processed_image_label.setFixedHeight(50)
        self.processed_image_label.setFixedWidth(50)
        self.image_container_2.setFixedHeight(700)
        self.image_container_2.setFixedWidth(350)

        self.init_ui()
    
    def init_ui(self):
        
        self.info_layout.addWidget(self.score_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.score_text, Qt.AlignBottom)
        self.info_layout.addWidget(self.line_0)
        self.info_layout.addWidget(self.action_label, Qt.AlignBottom)
        self.info_layout.addWidget(self.recg_label,Qt.AlignBottom)

        self.image_container_1_layout.setSpacing(0)
        self.image_container_1_layout.addWidget(self.origin_image_label, Qt.AlignCenter)
        
        self.image_container_2_layout.setSpacing(0)
        self.image_container_2_layout.addWidget(self.processed_image_label, Qt.AlignCenter)

        self.set_default_image(self.origin_image_label)
        self.set_default_image(self.processed_image_label)

        self.media_container_layout.addWidget(self.image_container_1)
        self.media_container_layout.addWidget(self.line)
        self.media_container_layout.addWidget(self.image_container_2)

        self.layout.setSpacing(0)
        self.layout.addWidget(self.info_widgets)
        self.layout.addWidget(self.media_container)
    
    def set_default_image(self, label):
        image = QPixmap('./source/image/pic_none.png')
        # image.load(image_path)
        label.setPixmap(image)
        label.setScaledContents(True)


    def set_image(self):
        image_file,_ = QFileDialog.getOpenFileName(self, "Select The Path: ", './data')
        image = QPixmap(image_file)
        # image.load(image_path)
        self.origin_image_label.setPixmap(image)
        self.processed_image_label.setPixmap(image)

        self.origin_image_label.setFixedWidth(350)
        self.origin_image_label.setFixedHeight(700)
        self.processed_image_label.setFixedHeight(700)
        self.processed_image_label.setFixedWidth(350)

        self.origin_image_label.setScaledContents(True)
        self.processed_image_label.setScaledContents(True)