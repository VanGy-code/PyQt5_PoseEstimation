#  ____                 ___       __                          
# /\  _`\           __ /\_ \     /\ \  __                     
# \ \ \L\ \  __  __/\_\\//\ \    \_\ \/\_\    ___      __     
#  \ \  _ <'/\ \/\ \/\ \ \ \ \   /'_` \/\ \ /' _ `\  /'_ `\   
#   \ \ \L\ \ \ \_\ \ \ \ \_\ \_/\ \L\ \ \ \/\ \/\ \/\ \L\ \  
#    \ \____/\ \____/\ \_\/\____\ \___,_\ \_\ \_\ \_\ \____ \ 
#     \/___/  \/___/  \/_/\/____/\/__,_ /\/_/\/_/\/_/\/___L\ \
#                                                      /\____/
#                                                      \_/__/  
from logging import setLoggerClass
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from qt_material import apply_stylesheet, QtStyleTools

from app.Activitys.VideoBaseActivity import VideoBaseActivity
from app.Activitys.ImageBaseActivity import ImageBaseActivity
from app.Activitys.CameraBaseActivity import CameraBaseActivity

from app.Components.AdviceBubbleBar import AdviceBubbleTextBar

from config import font_style


class MainUi(QMainWindow, QtStyleTools):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1400, 750)
        self.setObjectName("MainWindow")
        # self.setWindowIcon(QIcon('source/image/logo.png'))

        """
        界面样式
        """
        extra = {

            # Button colors
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#17a2b8',

            # Font
            'font-family': 'Roboto',
        }
        """
        创建布局
        """
        # 创建窗口主部件
        self.main_widget = QWidget()
        # 创建主部件的网格布局
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        # self.apply_stylesheet(self.main_widget, 'dark_amber.xml', invert_secondary=True, extra=extra)
        self.apply_stylesheet(self.main_widget, 'dark_amber.xml', extra=extra)
        """
        左侧导航页面
        """
        style_sheets = self.styleSheet()
        self.left_toolbar = self.addToolBar('')
        # self.left_toolbar.setStyleSheet("QToolBar{padding-bottom:8px;}")
        self.left_toolbar.setOrientation(Qt.Orientation.Vertical)
        self.left_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # self.left_toolbar.setIconSize(QSize(20, 20))

        self.logo = QAction(QIcon('./source/image/badminton.png'), 'BadMinTon', self)
        # self.logo.setFont()
        self.font_style = font_style
        self.logo.setFont(QFont(self.font_style, 20))
        self.logo.setCheckable(True)
        self.logo.setChecked(True)
        
        self.import_media = QAction(QIcon('./source/image/import_light.png'),'Import', self)
        self.import_media.setFont(QFont(self.font_style, 16))
        
        self.export_media = QAction(QIcon('./source/image/export_light.png'),'Export', self)
        self.export_media.setFont(QFont(self.font_style, 16))
        # self.export_media.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        """
        中间显示区域
        """
        self.middle_widget = QTabWidget()

        # 加载本地照片
        self.image_base_activity = ImageBaseActivity()
        # 本地视频
        self.video_base_activity = VideoBaseActivity()

        # 相机流
        self.camera_base_activity = CameraBaseActivity()

        # TODO: 视频流
        # self.stream_base_activity = QWidget()
        
        """
        分割线
        """
        self.line_1 = QFrame()
        self.line_1.setFrameShape(QFrame.VLine)
        self.line_1.setFrameShadow(QFrame.Sunken)
        self.line_1.setObjectName("line")
        """
        右侧建议评论区
        """
        self.right_widget = QWidget()
        self.right_layout = QHBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        # TODO
        self.advice_bubble = AdviceBubbleTextBar() 

        """
        初始化用户界面
        """
        self.init_ui()
        self.init_action_listener()

    def init_ui(self):

        # 左侧部件
        self.left_toolbar.addAction(self.logo)
        self.left_toolbar.addSeparator()
        self.left_toolbar.addAction(self.import_media)
        self.left_toolbar.addAction(self.export_media)
        self.main_layout.addWidget(self.left_toolbar)
        # self.main_layout.addStretch(5)

        # 中间部件
        self.middle_widget.addTab(self.image_base_activity, 'Image')
        self.middle_widget.addTab(self.video_base_activity, 'Video')
        # self.middle_widget.addTab(self.stream_base_activity, 'Stream')
        self.middle_widget.addTab(self.camera_base_activity, 'Camera')

        self.main_layout.addWidget(self.middle_widget)

        # self.main_layout.addStretch(2)
        self.main_layout.addWidget(self.line_1)
        # 右侧部件
        self.right_layout.addWidget(self.advice_bubble)
        self.main_layout.addWidget(self.right_widget)

        self.middle_widget.setCurrentIndex(0)

        # 设置窗口主部件
        self.center()
        self.setCentralWidget(self.main_widget)

    def import_action_clicked_listener(self):
        # 导入点击响应
        if self.middle_widget.currentIndex() == 0:
            self.image_base_activity.set_image()
            
        elif self.middle_widget.currentIndex() == 1:
            self.video_base_activity.setVideo()

    def export_action_clicked_listener(self):
        # TODO：识别视频导出点击响应
        pass

    def init_action_listener(self):
        # 绑定左侧导航栏按钮响应事件
        # self.left_button_1.clicked.connect(self.on_recommend_page_button_click_listener)
        self.import_media.triggered.connect(lambda: self.import_action_clicked_listener())
        self.export_media.triggered.connect(lambda: self.export_action_clicked_listener())

    def center(self):
        """
        获取桌面长宽
        获取窗口长宽
        移动
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)