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


class BubbleMessage(QWidget):
    def __init__(self, msg='Unknown Message', font='Arial'):
        super().__init__()

        self.font = QFont(font)
        self.font.setPointSize(12)

        self.icon_rect = QRect(0, 0, 20, 20)
        self.avater = QPixmap('./source/image/avater.jpeg')

        self.text_message = msg
        self.msg_line_height = 0
        self.bubble_rect_width = 0
        self.msg_rect_width = 0
        self.msg_text_width = 0
        self.msg_space_width = 0
        self.message_loaded = False

        self.msg_text_rect = QRectF(0, 0, 20, 20)
        self.msg_rect = QRect(0, 0, 20, 20)

        # 建议正在加载
        self.movie_label = QLabel()
        self.loading_movie = QMovie(self)
        self.loading_movie.setFileName('./source/gif/loading.gif')
        self.loading_movie.setScaledSize(QSize(16, 16))
        self.movie_label.setMovie(self.loading_movie)
        # self.movie_label.setAttribute(Qt.WA_TranslucentBackgroud, True)
        self.movie_label.setAutoFillBackground(False)
        # self.loadingMovie.start()

        # 绘制评论建议框
        # self.painer = QPainter(self)

    def paintEvent(self, event):
        '''
        description: 绘制Item
        param {*}
        return {*}
        '''
        painter = QPainter(self)
        # 画笔消除锯齿
        painter.setRenderHints(painter.Antialiasing
                               | painter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.gray))

        # 绘制头像
        # painter.drawPixmap(0, 0, self.avater)
        painter.drawPixmap(self.icon_rect, self.avater)

        # 绘制框边缘阴影
        shadow_color = QColor(255, 255, 255)

        defeat_color = QColor(234, 234, 234)

        # 绘制框

        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(
            self.msg_rect.x() - 1,
            self.msg_rect.y() - 1,
            self.msg_rect.width() + 2,
            self.msg_rect.height() + 2,
            4,
            4,
        )

        # 绘制气泡三角
        points = [
            QPointF(
                self.rectangle_rect.x(),
                self.rectangle_rect.y() + self.rectangle_rect.height() / 2,
            ),
            QPointF(
                self.rectangle_rect.x() + self.rectangle_rect.width(),
                self.rectangle_rect.y(),
            ),
            QPointF(self.rectangle_rect.x() + self.rectangle_rect.width(),
                    self.rectangle_rect.y() + self.rectangle_rect.height()),
        ]

        pen = QPen()
        pen.setColor(shadow_color)
        painter.setPen(pen)
        painter.drawPolygon(QPolygonF(points))

        # 绘制文本内容
        text_pen = QPen()
        text_pen.setColor(QColor(51, 51, 51))
        painter.setPen(text_pen)
        text_option = QTextOption(Qt.AlignLeft | Qt.AlignVCenter)
        text_option.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        painter.setFont(self.font)
        painter.drawText(self.msg_text_rect,
                         self.text_message,
                         option=text_option)

    def set_rect(self):
        '''
        description: 设置整个Item的内框与外框
        param {*}
        return {*}
        '''
        min_height = 40
        icon_length = 40

        # icon_coordinate
        icon_x = 2
        icon_y = 2
        icon_padding_right = 10

        # 字符串相对于文本框的padding
        text_padding_top_bottom = 10
        text_padding_left_right = 10

        # Box_padding
        rect_y = 5
        rectangle_width = 6
        rectangle_height = 10
        rect_padding_bottom = 5

        # 文本框的最大宽度 = ListItem的最大宽度 - 两端头像区域所占宽度
        self.bubble_rect_width = self.width() - (icon_length + icon_x +
                                                 icon_padding_right)

        # 字符串的显示长度 = 文本框的宽度 - 字符串与文本框两端的空隙
        self.msg_rect_width = self.bubble_rect_width - rectangle_width
        self.msg_text_width = self.msg_rect_width - text_padding_left_right

        # 左侧头像框
        self.icon_rect = QRect(icon_x, icon_y, icon_length, icon_length)

        # 获取文本长度信息
        message_rect_size = self.get_string_status()

        message_rect_height = message_rect_size.height()
        bubble_rect_height = message_rect_height + rect_y + rect_padding_bottom + 2 * text_padding_top_bottom
        if bubble_rect_height < min_height:
            bubble_rect_height = min_height

        # rectangle
        rectangle_x = icon_length + icon_x + icon_padding_right + 1
        rectangle_y = rect_y + 1

        # 气泡三角框
        self.rectangle_rect = QRectF(rectangle_x, rectangle_y, rectangle_width,
                                     rectangle_height)

        min_msg_rect_width = message_rect_size.width() + text_padding_left_right + rectangle_width
        if message_rect_size.width() > self.msg_text_width:
            min_msg_rect_width = self.bubble_rect_width

        self.msg_rect = QRectF(
            self.rectangle_rect.x() + self.rectangle_rect.width(), rect_y,
            min_msg_rect_width + 0.5 * text_padding_left_right,
            bubble_rect_height - 1.2 * rect_padding_bottom)

        self.msg_text_rect = QRectF(
            self.msg_rect.x() + text_padding_left_right,
            self.msg_rect.y() + text_padding_top_bottom,
            message_rect_size.width() + text_padding_left_right,
            message_rect_height * 1.2)

        return QSize(min_msg_rect_width - rectangle_width,
                     bubble_rect_height + 2.5 * rect_padding_bottom)

    def get_string_status(self):
        '''
        description: get the message attributes
        param {*}
        return {*}
        '''
        message = self.text_message
        font_metrics = QFontMetricsF(self.font)
        self.msg_line_height = font_metrics.lineSpacing()

        # total line auto_add_lineber
        line_count = message.count('\n')
        # print('line count:' + str(line_count))
        max_line_width = font_metrics.width(message)

        if line_count == 0:
            # one line
            # defeat max_line_width
            if max_line_width > self.bubble_rect_width:
                # 当文本长度大于文本框宽度时，换行显示
                max_line_width = self.msg_text_width
                length = self.msg_text_width / font_metrics.width(" ")
                # 文本在文本框中的行数
                auto_add_line = font_metrics.width(
                    message) / self.msg_text_width

                # print('auto added line: ' + str(auto_add_line))

                # 除了文本自带的换行，还要加上因为超出文本框边界进行的换行
                line_count += auto_add_line

                # 字符串重新排版
                redraft_message = ""
                for i in range(auto_add_line):
                    # 从中间截取字符串
                    redraft_message += message[i * length:(i + 1) *
                                               length] + "\n"

                self.text_message.replace(message, redraft_message)
        else:
            # multi-line
            str_list = self.text_message.split("\n")
            for i in range(line_count + 1):
                message = str_list[i]

                if font_metrics.width(message) > max_line_width:
                    max_line_width = font_metrics.width(message)

                if font_metrics.width(message) > self.msg_text_width:
                    max_line_width = self.msg_text_width
                    length = self.msg_text_width / font_metrics.width(" ")

                    auto_add_line = (
                        (i + auto_add_line) * font_metrics.width(" ") +
                        font_metrics.width(message)) / self.msg_text_width
                    line_count += auto_add_line

                    # 对文本信息进行重新排版
                    redraft_message = ""
                    for i in range(auto_add_line):
                        redraft_message += message[i * length:(i + 1) *
                                                   length] + "\n"

                    # 字符串重新排版
                    self.text_message.replace(message, redraft_message)

        # print(self.text_message)
        return QSize(max_line_width + self.msg_space_width,
                     (line_count + 1) * self.msg_line_height)

    def set_text(self, msg):
        '''
        description: 设置输出的字符串相关属性
        param {*}
        return {*}
        '''
        self.text_message = msg
        self.movie_label.setVisible(False)
        self.paint_event()

    def set_text_success(self):
        '''
        description: 成功设置字符串返回信息
        param {*}
        return {*}
        '''
        self.movie_label.setVisible(False)
        self.loading_movie.stop()
        self.message_loaded = True
