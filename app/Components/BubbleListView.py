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

from app.Components.BubbleMessage import BubbleMessage

class BubbleListView(QListWidget):
    def __init__(self):
        super().__init__()
        self.update()
    
    def update(self):
        # TODO: 实时加入列表Item
        self.add_message('!!!!!!!')
        self.add_message('We made it\nCrazy Task!!!')


    def item_clicked(self, item):
        print('Selcted ')

    def add_message(self, input_message='Unknow Message', time= '00:00:00'):
        new_item = QListWidgetItem(self)
        new_message = BubbleMessage(input_message)
        new_message.setFixedWidth(self.width())
        size = new_message.set_rect()
        print(str(size))
        # new_item.setSizeHint(QSize(100,100))
        new_item.setSizeHint(size)
        self.setItemWidget(new_item, new_message)
