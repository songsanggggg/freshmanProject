from src.BasePage import BasePage
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Slot
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

# 数据处理页面
class DataProcessPage(BasePage):
    
    def __init__(self, pages=None, stackedWidget=None):
        super().__init__('./ui/dataProcessPage.ui', pages, stackedWidget)
        self.ui.datasetSelectBtn.clicked.connect(self.importDataset)
        self.ui.missingItemsCheckBtn.clicked.connect(self.checkMissingItems)
        self.ui.duplicatesProcessingBtn.clicked.connect(self.checkDuplicates)
        self.ui.datatypeCheckBtn.clicked.connect(self.checkDataTypes)
        self.ui.pictureGenerationBtn.clicked.connect(self.generatePicture)
        self.datasetPath = None

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
    def checkMissingItems(self):
        if self.datasetPath is None:
            QMessageBox.warning(self, '错误', '请先选择数据集文件', QMessageBox.Ok)
            return

        data = pd.read_csv(self.datasetPath)
        missingValues = data.isnull().sum()
        dataCleaned = data.dropna()
        dataCleaned.to_csv(self.datasetPath, index=False)
        QMessageBox.information(
            self,
            '数据处理结果',
            f'缺失值统计:\n{missingValues}\n\n'
            f'已清理数据集，清理后的数据集包含 {len(dataCleaned)} 条记录。\n'
            f'缺失项所在的行已被删除并保存。',
            QMessageBox.Ok
        )

    @Slot()
    def checkDuplicates(self):
        if self.datasetPath is None:
            QMessageBox.warning(self, '错误', '请先选择数据集文件', QMessageBox.Ok)
            return

        data = pd.read_csv(self.datasetPath)
        duplicates = data.duplicated().sum()
        if duplicates > 0:
            dataCleaned = data.drop_duplicates()
            dataCleaned.to_csv(self.datasetPath, index=False)
            QMessageBox.information(
                self,
                '数据处理结果',
                f'发现 {duplicates} 条重复记录，已删除并保存清理后的数据集。',
                QMessageBox.Ok
            )
        else:
            QMessageBox.information(
                self,
                '数据处理结果',
                '未发现重复记录。',
                QMessageBox.Ok
            )

    @Slot()
    def checkDataTypes(self):
        if self.datasetPath is None:
            QMessageBox.warning(self, '错误', '请先选择数据集文件', QMessageBox.Ok)
            return

        data = pd.read_csv(self.datasetPath)
        dataTypes = data.dtypes
        QMessageBox.information(
            self,
            '数据类型检查',
            f'数据集中的列及其数据类型:\n{dataTypes}',
            QMessageBox.Ok
        )

    @Slot()
    def generatePicture(self):
        if self.datasetPath is None:
            QMessageBox.warning(self, '错误', '请先选择数据集文件', QMessageBox.Ok)
            return

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.componentName = self.ui.componentSelectionBox.currentText()
        data = pd.read_csv(self.datasetPath)
        filtered_data = data[data['器件类型'] == self.componentName]
        plt.figure(figsize=(8, 5))
        center_temp = filtered_data['中心温度(℃)'].values
        pin_temp = filtered_data['引脚温度(℃)'].values
        time = filtered_data['时间(s)'].values
        window_length = 7 if len(center_temp) >= 7 else (len(center_temp) // 2 * 2 + 1)
        smoothed_center = savgol_filter(center_temp, window_length, polyorder = 2)
        smoothed_pin = savgol_filter(pin_temp, window_length, polyorder = 2)
        plt.plot(time, smoothed_center, marker='o', markersize=2, label='中心温度(℃) (平滑)')
        plt.plot(time, smoothed_pin, marker='s', markersize=2, label='引脚温度(℃) (平滑)')
        plt.xlabel('时间(s)')
        plt.ylabel('温度(℃)')
        plt.title(f'{self.componentName}温度变化曲线')
        plt.legend()
        plt.tight_layout()
        plt.show()
