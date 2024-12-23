# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'left_column.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_LeftColumn(object):
    def setupUi(self, LeftColumn):
        if not LeftColumn.objectName():
            LeftColumn.setObjectName(u"LeftColumn")
        LeftColumn.resize(569, 600)
        self.main_pages_layout = QVBoxLayout(LeftColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(LeftColumn)
        self.menus.setObjectName(u"menus")
        self.menu_1 = QWidget()
        self.menu_1.setObjectName(u"menu_1")
        self.verticalLayout = QVBoxLayout(self.menu_1)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.btn_1_widget = QWidget(self.menu_1)
        self.btn_1_widget.setObjectName(u"btn_1_widget")
        self.btn_1_widget.setMinimumSize(QSize(0, 40))
        self.btn_1_widget.setMaximumSize(QSize(16777215, 40))
        self.btn_1_layout = QVBoxLayout(self.btn_1_widget)
        self.btn_1_layout.setSpacing(0)
        self.btn_1_layout.setObjectName(u"btn_1_layout")
        self.btn_1_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_1_widget)

        self.btn_2_widget = QWidget(self.menu_1)
        self.btn_2_widget.setObjectName(u"btn_2_widget")
        self.btn_2_widget.setMinimumSize(QSize(0, 40))
        self.btn_2_widget.setMaximumSize(QSize(16777215, 40))
        self.btn_2_layout = QVBoxLayout(self.btn_2_widget)
        self.btn_2_layout.setSpacing(0)
        self.btn_2_layout.setObjectName(u"btn_2_layout")
        self.btn_2_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_2_widget)

        self.btn_3_widget = QWidget(self.menu_1)
        self.btn_3_widget.setObjectName(u"btn_3_widget")
        self.btn_3_widget.setMinimumSize(QSize(0, 40))
        self.btn_3_widget.setMaximumSize(QSize(16777215, 40))
        self.btn_3_layout = QVBoxLayout(self.btn_3_widget)
        self.btn_3_layout.setSpacing(0)
        self.btn_3_layout.setObjectName(u"btn_3_layout")
        self.btn_3_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_3_widget)

        self.label_1 = QLabel(self.menu_1)
        self.label_1.setObjectName(u"label_1")
        font = QFont()
        font.setPointSize(16)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"font-size: 16pt")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_1)

        self.menus.addWidget(self.menu_1)
        self.menu_setting = QWidget()
        self.menu_setting.setObjectName(u"menu_setting")
        self.layoutWidget = QWidget(self.menu_setting)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 541, 240))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.select_import_file = QWidget(self.layoutWidget)
        self.select_import_file.setObjectName(u"select_import_file")
        self.select_import_file.setMinimumSize(QSize(0, 40))
        self.select_import_file.setMaximumSize(QSize(16777215, 40))
        self.select_import_file_layout = QVBoxLayout(self.select_import_file)
        self.select_import_file_layout.setSpacing(0)
        self.select_import_file_layout.setObjectName(u"select_import_file_layout")
        self.select_import_file_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.select_import_file)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_group = QLabel(self.layoutWidget)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setMinimumSize(QSize(0, 40))
        self.label_group.setMaximumSize(QSize(16777215, 40))
        self.label_group.setFont(font)
        self.label_group.setStyleSheet(u"font-size: 16pt")
        self.label_group.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_group)

        self.select_group = QWidget(self.layoutWidget)
        self.select_group.setObjectName(u"select_group")
        self.select_group.setMinimumSize(QSize(0, 40))
        self.select_group.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_4.addWidget(self.select_group)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_project = QLabel(self.layoutWidget)
        self.label_project.setObjectName(u"label_project")
        self.label_project.setMinimumSize(QSize(0, 40))
        self.label_project.setMaximumSize(QSize(16777215, 40))
        self.label_project.setFont(font)
        self.label_project.setStyleSheet(u"font-size: 16pt")
        self.label_project.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_project)

        self.select_project = QWidget(self.layoutWidget)
        self.select_project.setObjectName(u"select_project")
        self.select_project.setMinimumSize(QSize(0, 40))
        self.select_project.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout.addWidget(self.select_project)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_timer = QLabel(self.layoutWidget)
        self.label_timer.setObjectName(u"label_timer")
        self.label_timer.setMinimumSize(QSize(0, 40))
        self.label_timer.setMaximumSize(QSize(16777215, 40))
        self.label_timer.setFont(font)
        self.label_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_timer)

        self.select_timer_item = QWidget(self.layoutWidget)
        self.select_timer_item.setObjectName(u"select_timer_item")
        self.select_timer_item.setMinimumSize(QSize(0, 40))
        self.select_timer_item.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.select_timer_item.setFont(font1)
        self.select_timer_item_layout = QVBoxLayout(self.select_timer_item)
        self.select_timer_item_layout.setSpacing(0)
        self.select_timer_item_layout.setObjectName(u"select_timer_item_layout")
        self.select_timer_item_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.select_timer_item)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_count = QLabel(self.layoutWidget)
        self.label_count.setObjectName(u"label_count")
        self.label_count.setMinimumSize(QSize(0, 40))
        self.label_count.setMaximumSize(QSize(16777215, 40))
        self.label_count.setFont(font)
        self.label_count.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_count)

        self.select_current_count = QWidget(self.layoutWidget)
        self.select_current_count.setObjectName(u"select_current_count")
        self.select_current_count.setMinimumSize(QSize(0, 40))
        self.select_current_count.setMaximumSize(QSize(16777215, 40))
        self.select_current_count_layout = QVBoxLayout(self.select_current_count)
        self.select_current_count_layout.setSpacing(0)
        self.select_current_count_layout.setObjectName(u"select_current_count_layout")
        self.select_current_count_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3.addWidget(self.select_current_count)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.menus.addWidget(self.menu_setting)
        self.menu_2 = QWidget()
        self.menu_2.setObjectName(u"menu_2")
        self.verticalLayout_2 = QVBoxLayout(self.menu_2)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.btn_4_widget = QWidget(self.menu_2)
        self.btn_4_widget.setObjectName(u"btn_4_widget")
        self.btn_4_widget.setMinimumSize(QSize(0, 40))
        self.btn_4_widget.setMaximumSize(QSize(16777215, 40))
        self.btn_4_layout = QVBoxLayout(self.btn_4_widget)
        self.btn_4_layout.setSpacing(0)
        self.btn_4_layout.setObjectName(u"btn_4_layout")
        self.btn_4_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.btn_4_widget)

        self.label_2 = QLabel(self.menu_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font-size: 16pt")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.menu_2)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setPointSize(9)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"font-size: 9pt")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.menus.addWidget(self.menu_2)

        self.main_pages_layout.addWidget(self.menus)


        self.retranslateUi(LeftColumn)

        self.menus.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(LeftColumn)
    # setupUi

    def retranslateUi(self, LeftColumn):
        LeftColumn.setWindowTitle(QCoreApplication.translate("LeftColumn", u"Form", None))
        self.label_1.setText(QCoreApplication.translate("LeftColumn", u"Menu 1 - Left Menu", None))
        self.label_group.setText(QCoreApplication.translate("LeftColumn", u"\u7ec4\u522b", None))
        self.label_project.setText(QCoreApplication.translate("LeftColumn", u"\u6bd4\u8d5b\u9879\u76ee", None))
        self.label_timer.setText(QCoreApplication.translate("LeftColumn", u"\u6bd4\u8d5b\u65b9\u5f0f", None))
        self.label_count.setText(QCoreApplication.translate("LeftColumn", u"\u8bf7\u8f93\u5165\u6bd4\u8d5b\u6b21\u6570", None))
        self.label_2.setText(QCoreApplication.translate("LeftColumn", u"Menu 2 - Left Menu", None))
        self.label_3.setText(QCoreApplication.translate("LeftColumn", u"This is just an example menu.\n"
"Add Qt Widgets or your custom widgets here.", None))
    # retranslateUi

