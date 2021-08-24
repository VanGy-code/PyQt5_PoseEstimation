#  ____                 ___       __                          
# /\  _`\           __ /\_ \     /\ \  __                     
# \ \ \L\ \  __  __/\_\\//\ \    \_\ \/\_\    ___      __     
#  \ \  _ <'/\ \/\ \/\ \ \ \ \   /'_` \/\ \ /' _ `\  /'_ `\   
#   \ \ \L\ \ \ \_\ \ \ \ \_\ \_/\ \L\ \ \ \/\ \/\ \/\ \L\ \  
#    \ \____/\ \____/\ \_\/\____\ \___,_\ \_\ \_\ \_\ \____ \ 
#     \/___/  \/___/  \/_/\/____/\/__,_ /\/_/\/_/\/_/\/___L\ \
#                                                      /\____/
#                                                      \_/__/  
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app.Components.BubbleListView import BubbleListView

class AdviceBubbleTextBar(QWidget):

    def __init__(self):
        super().__init__()
        self.font_style = 'Arial'

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumWidth(200)
        

        self.name_label = QLabel('Action Advice')
        self.name_label.setFont(QFont(QFont(self.font_style, 18, 75)))
        
        self.line_1 = QFrame()
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)
        self.line_1.setObjectName("line")

        self.list_view = BubbleListView()
        self.list_view.itemClicked.connect(self.list_view.item_clicked)
        # TODO：自动加载动作建议

        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.line_1)
        self.layout.addWidget(self.list_view)
        # self.layout.addStretch(6)

    def add_item(self):
        pass