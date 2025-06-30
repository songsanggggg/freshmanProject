from PySide6.QtWidgets import QWidget, QMessageBox, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot
from src.Config import __version__
from PySide6.QtWidgets import QApplication

# 基础页面
class BasePage(QWidget):

    def __init__(self, uiFile, pages=None, stackedWidget=None):
        super().__init__()
        self.pages = pages
        self.stackedWidget = stackedWidget
        self.ui = QUiLoader().load(uiFile)
        self.ui.setWindowTitle(f'回流焊仿真软件 V{__version__}')
        self.ui.title.setText(f'回流焊仿真软件 V{__version__}')
        self.ui.exitSystem.clicked.connect(self.exitSystem)
        self.ui.modelPage.clicked.connect(self.showModelPage)
        self.ui.dataProcessPage.clicked.connect(self.showDataProcessPage)
        self.ui.argumentPage.clicked.connect(self.showArgumentPage)
    

    @Slot()
    def showModelPage(self):
        self.stackedWidget.setCurrentWidget(self.pages['model'].ui)

    @Slot()
    def showDataProcessPage(self):
        self.stackedWidget.setCurrentWidget(self.pages['data_process'].ui)

    @Slot()
    def showArgumentPage(self):
        self.stackedWidget.setCurrentWidget(self.pages['argument'].ui)

    @Slot()
    def exitSystem(self):
        choice = QMessageBox.question(self, '退出系统', '是否退出系统？', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            QApplication.instance().quit()