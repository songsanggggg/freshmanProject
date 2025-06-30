from src.BasePage import BasePage
from PySide6.QtCore import Slot
from src.temperaturePrediction import TemperaturePrediction
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox
import pandas as pd

# 模型页面
class ModelPage(BasePage):
    
    def __init__(self, pages=None, stackedWidget=None):
        super().__init__('./ui/modelPage.ui', pages, stackedWidget)
        self.ui.modelBtn.clicked.connect(self.startModeling)
        self.ui.datasetSelectBtn.clicked.connect(self.importDataset)

    @Slot()
    def importDataset(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
        if selected_files:
            self.datasetPath = selected_files[0]
            self.ui.datasetPath.setText(self.datasetPath.split('/')[-1])
        else:
            self.datasetPath = None
            self.ui.datasetPath.setText('未选择文件')

    @Slot()
    def startModeling(self):
        if self.datasetPath is None:
            QMessageBox.warning(self, '错误', '请先选择数据集文件', QMessageBox.Ok)
            return
        
        self.compomentName = self.ui.compomentBox.currentText()
        self.place = self.ui.placeBox.currentText()

        predictor = TemperaturePrediction(self.datasetPath, component_type=self.compomentName)
        predictor.evaluate(temperature_type=f'{self.place}(℃)')
