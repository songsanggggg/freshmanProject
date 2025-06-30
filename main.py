from PySide6.QtWidgets import QApplication, QMessageBox, QStackedWidget, QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot
import os
import PySide6
from qt_material import apply_stylesheet
from src.Config import __version__
from src.ModelPage import ModelPage
from src.DataProcessPage import DataProcessPage
from src.ArgumentPage import ArgumentPage
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(os.path.dirname(PySide6.__file__), "plugins", "platforms")



# 主窗口
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('./ui/main.ui')
        self.setWindowTitle(f'回流焊仿真软件 V{__version__}')
        self.ui.title.setText(f'回流焊仿真软件 V{__version__}')

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.ui)

        self.pages = {}
        self.pages['model'] = ModelPage(self.pages, self.stackedWidget)
        self.pages['data_process'] = DataProcessPage(self.pages, self.stackedWidget)
        self.pages['argument'] = ArgumentPage(self.pages, self.stackedWidget)


        for page in self.pages.values():
            self.stackedWidget.addWidget(page.ui)

        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

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
            app.quit()


# 应用程序入口
if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MainWindow()
    apply_stylesheet(app, theme='dark_cyan.xml')
    mainWindow.show()
    app.exec()
