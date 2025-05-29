# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QMainWindow, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(740, 525)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.sidebar = QWidget(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.label_scientiflow = QLabel(self.sidebar)
        self.label_scientiflow.setObjectName(u"label_scientiflow")
        self.label_scientiflow.setStyleSheet(u"font-size: 22pt; font-weight: bold; margin: 20px 0px 20px 0px;")
        self.label_scientiflow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebarLayout.addWidget(self.label_scientiflow)

        self.btn_jobs = QPushButton(self.sidebar)
        self.btn_jobs.setObjectName(u"btn_jobs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_jobs.sizePolicy().hasHeightForWidth())
        self.btn_jobs.setSizePolicy(sizePolicy)
        self.btn_jobs.setMinimumSize(QSize(0, 0))

        self.sidebarLayout.addWidget(self.btn_jobs)

        self.verticalSpacer_2 = QSpacerItem(5, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.verticalSpacer_2)

        self.btn_manage_containers = QPushButton(self.sidebar)
        self.btn_manage_containers.setObjectName(u"btn_manage_containers")
        sizePolicy.setHeightForWidth(self.btn_manage_containers.sizePolicy().hasHeightForWidth())
        self.btn_manage_containers.setSizePolicy(sizePolicy)

        self.sidebarLayout.addWidget(self.btn_manage_containers)

        self.verticalSpacer_3 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.verticalSpacer_3)

        self.btn_settings = QPushButton(self.sidebar)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy)

        self.sidebarLayout.addWidget(self.btn_settings)

        self.verticalSpacer_4 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.verticalSpacer_4)

        self.btn_logout = QPushButton(self.sidebar)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)

        self.sidebarLayout.addWidget(self.btn_logout)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.verticalSpacer)


        self.mainLayout.addWidget(self.sidebar)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_jobs = QWidget()
        self.page_jobs.setObjectName(u"page_jobs")
        self.jobsLayout = QVBoxLayout(self.page_jobs)
        self.jobsLayout.setObjectName(u"jobsLayout")
        self.executionOptionsLayout = QHBoxLayout()
        self.executionOptionsLayout.setObjectName(u"executionOptionsLayout")
        self.executionOptionsLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.radio_parallel = QRadioButton(self.page_jobs)
        self.radio_parallel.setObjectName(u"radio_parallel")
        self.radio_parallel.setChecked(True)

        self.executionOptionsLayout.addWidget(self.radio_parallel)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.executionOptionsLayout.addItem(self.horizontalSpacer)

        self.radio_synchronous = QRadioButton(self.page_jobs)
        self.radio_synchronous.setObjectName(u"radio_synchronous")

        self.executionOptionsLayout.addWidget(self.radio_synchronous)

        self.horizontalSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.executionOptionsLayout.addItem(self.horizontalSpacer1)

        self.btn_execute = QPushButton(self.page_jobs)
        self.btn_execute.setObjectName(u"btn_execute")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_execute.sizePolicy().hasHeightForWidth())
        self.btn_execute.setSizePolicy(sizePolicy1)
        self.btn_execute.setMinimumSize(QSize(150, 0))

        self.executionOptionsLayout.addWidget(self.btn_execute)


        self.jobsLayout.addLayout(self.executionOptionsLayout)

        self.table_jobs = QTableWidget(self.page_jobs)
        if (self.table_jobs.columnCount() < 3):
            self.table_jobs.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_jobs.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_jobs.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_jobs.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_jobs.setObjectName(u"table_jobs")
        self.table_jobs.setMaximumSize(QSize(16777215, 16777215))
        self.table_jobs.setRowCount(0)
        self.table_jobs.setColumnCount(3)
        self.table_jobs.horizontalHeader().setStretchLastSection(True)

        self.jobsLayout.addWidget(self.table_jobs)

        self.verticalSpacer_logs_top = QSpacerItem(20, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.jobsLayout.addItem(self.verticalSpacer_logs_top)

        self.textBrowser_logs = QTextBrowser(self.page_jobs)
        self.textBrowser_logs.setObjectName(u"textBrowser_logs")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.textBrowser_logs.sizePolicy().hasHeightForWidth())
        self.textBrowser_logs.setSizePolicy(sizePolicy2)
        self.textBrowser_logs.setMaximumSize(QSize(16777215, 60))

        self.jobsLayout.addWidget(self.textBrowser_logs)

        self.verticalSpacer_logs_bottom = QSpacerItem(20, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.jobsLayout.addItem(self.verticalSpacer_logs_bottom)

        self.stackedWidget.addWidget(self.page_jobs)
        self.page_manage_containers = QWidget()
        self.page_manage_containers.setObjectName(u"page_manage_containers")
        self.containersLayout = QVBoxLayout(self.page_manage_containers)
        self.containersLayout.setObjectName(u"containersLayout")
        self.btn_delete_containers = QPushButton(self.page_manage_containers)
        self.btn_delete_containers.setObjectName(u"btn_delete_containers")

        self.containersLayout.addWidget(self.btn_delete_containers)

        self.table_containers = QTableWidget(self.page_manage_containers)
        if (self.table_containers.columnCount() < 2):
            self.table_containers.setColumnCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_containers.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_containers.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        self.table_containers.setObjectName(u"table_containers")
        self.table_containers.setRowCount(0)
        self.table_containers.setColumnCount(2)
        self.table_containers.horizontalHeader().setStretchLastSection(True)

        self.containersLayout.addWidget(self.table_containers)

        self.stackedWidget.addWidget(self.page_manage_containers)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.settingsLayout = QVBoxLayout(self.page_settings)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.verticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsLayout.addItem(self.verticalSpacer2)

        self.stackedWidget.addWidget(self.page_settings)
        self.page_logout = QWidget()
        self.page_logout.setObjectName(u"page_logout")
        self.logoutLayout = QVBoxLayout(self.page_logout)
        self.logoutLayout.setObjectName(u"logoutLayout")
        self.verticalSpacer3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.logoutLayout.addItem(self.verticalSpacer3)

        self.label_logout = QLabel(self.page_logout)
        self.label_logout.setObjectName(u"label_logout")
        self.label_logout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logoutLayout.addWidget(self.label_logout)

        self.stackedWidget.addWidget(self.page_logout)

        self.mainLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Scientiflow GUI", None))
        self.label_scientiflow.setText(QCoreApplication.translate("MainWindow", u"Scientiflow", None))
        self.btn_jobs.setText(QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.btn_manage_containers.setText(QCoreApplication.translate("MainWindow", u"Manage Containers", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.radio_parallel.setText(QCoreApplication.translate("MainWindow", u"Parallel", None))
        self.radio_synchronous.setText(QCoreApplication.translate("MainWindow", u"Synchronous", None))
        self.btn_execute.setText(QCoreApplication.translate("MainWindow", u"Execute", None))
        ___qtablewidgetitem = self.table_jobs.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Project Job ID", None));
        ___qtablewidgetitem1 = self.table_jobs.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Project Title", None));
        ___qtablewidgetitem2 = self.table_jobs.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Job Title", None));
        self.btn_delete_containers.setText(QCoreApplication.translate("MainWindow", u"Delete Containers", None))
        ___qtablewidgetitem3 = self.table_containers.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Container Name", None));
        self.label_logout.setText(QCoreApplication.translate("MainWindow", u"Click the Logout button in the sidebar to logout.", None))
    # retranslateUi

