from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot
from src.BasePage import BasePage
from src.Window import LoadingWindow
from src.GerberRender import gerberRenderWorker
from pygerber.gerberx3.api.v2 import FileTypeEnum, GerberFile, Project
import time


# 参数页面
class ArgumentPage(BasePage):
    
    def __init__(self, pages=None, stackedWidget=None):
        super().__init__('./ui/argumentPage.ui', pages, stackedWidget)
        self.ui.gerberImportBtn.clicked.connect(self.importGerberFile)
        self.ui.uploadTemperature.clicked.connect(self.gerTemperture)

    def importGerberFile(self):
        self.frontGerberFiles = []
        self.backGerberFiles = []
        self.gerberImportWindow = QDialog(self)
        self.gerberImportWindow.setWindowTitle('选择Gerber文件')
        self.gerberImportWindow.setFixedSize(400, 200)
        self.gerberImportWindow.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        layout = QVBoxLayout()
        self.frontButton = QPushButton('选择正面Gerber文件')
        self.fFileName =  QLabel('未选择文件')
        self.backButton = QPushButton('选择背面Gerber文件')
        self.bFileName = QLabel('未选择文件')
        self.uploadGerberFileButton = QPushButton('确认')
        self.uploadGerberFileButton.clicked.connect(self.uploadGerberFile)
        self.frontButton.clicked.connect(lambda: self.selectGerberFile('front'))
        self.backButton.clicked.connect(lambda: self.selectGerberFile('back'))
        layout.addWidget(self.frontButton)
        layout.addWidget(self.fFileName)
        layout.addWidget(self.backButton)
        layout.addWidget(self.bFileName)
        layout.addWidget(self.uploadGerberFileButton)
        self.gerberImportWindow.setLayout(layout)
        self.gerberImportWindow.exec()

    @Slot()
    def uploadGerberFile(self):
        self.fProject = []
        self.bProject = []
        if not self.frontGerberFiles or not self.backGerberFiles:
            QMessageBox.warning(self, '文件错误', '请上传正面和背面Gerber文件', QMessageBox.Yes)
            return
        for file in self.frontGerberFiles:
            if file.split('.')[-1].lower() not in ['gtl', 'gto', 'gts', 'gtp']:
                QMessageBox.warning(self, '文件错误', f'文件 {file} 不是有效的Gerber文件', QMessageBox.Yes)
                return
            self.fProject.append(GerberFile.from_file(file, FileTypeEnum.INFER_FROM_EXTENSION))
        for file in self.backGerberFiles:
            if file.split('.')[-1].lower() not in ['gbl', 'gbo', 'gbs', 'gbp']:
                QMessageBox.warning(self, '文件错误', f'文件 {file} 不是有效的Gerber文件', QMessageBox.Yes)
                return
            self.bProject.append(GerberFile.from_file(file, FileTypeEnum.INFER_FROM_EXTENSION))
        self.fProject = Project(self.fProject)
        self.bProject = Project(self.bProject)
        self.project = [self.fProject, self.bProject]
        currentTime = time.time()
        self.gerberImportWindow.close()
        self.renderGerberFiles(self.project, currentTime)
    
    @Slot()
    def selectGerberFile(self, side):
        if side == 'front':
            exention = 'Gerber文件 (*.gt* *.GT*)'
        elif side == 'back':
            exention = 'Gerber文件 (*.gb* *.GB*)'
        filePaths, _ = QFileDialog.getOpenFileNames(
            self,
            f'选择{side}Gerber文件',
            './example',
            exention
        )
        if filePaths:
            if side == 'front':
                self.fFileName.setText(f'{filePaths[0].split("/")[-1]}等共{len(filePaths)}个文件')
                self.frontGerberFiles = filePaths
            else:
                self.bFileName.setText(f'{filePaths[0].split("/")[-1]}等共{len(filePaths)}个文件')
                self.backGerberFiles = filePaths

    def renderGerberFiles(self, project, currentTime):
        self.loadingWindow = LoadingWindow()
        self.loadingWindow.show()
        self.worker = gerberRenderWorker(project, currentTime)
        self.worker.finished.connect(self.onRenderFinished)
        self.worker.start()

    def onRenderFinished(self, currentTime):
        self.loadingWindow.close()    
        self.showGerberFileImg(currentTime)
    
    def showGerberFileImg(self, currentTime):
        bottomImgPath = f"./tmp/{currentTime}-bottom.png"
        topImgPath = f"./tmp/{currentTime}-top.png"
        bottomPixmap = QPixmap(bottomImgPath)
        topPixmap = QPixmap(topImgPath)
        bottomPixmap = bottomPixmap.scaled(self.ui.bottomPic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        topPixmap = topPixmap.scaled(self.ui.topPic.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.bottomPic.setPixmap(bottomPixmap)
        self.ui.topPic.setPixmap(topPixmap)
        
        QMessageBox.information(self, '渲染完成', 'Gerber文件渲染完成', QMessageBox.Ok)
    
    @Slot()
    def gerTemperture(self):
        temperatures = []
        for i in range(1, 11):
            temp = getattr(self.ui, f'temperature{i}').text()
            if not temp:
                QMessageBox.warning(self, '输入错误', f'温度 {i} 不能为空', QMessageBox.Yes)
                return
            try:
                temperatures.append(float(temp))
            except ValueError:
                QMessageBox.warning(self, '输入错误', f'温度 {i} 不是有效的数字', QMessageBox.Yes)
                return
        print(temperatures)