from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox
import os


# gerber渲染类
class gerberRenderWorker(QThread):
    finished = Signal(float)

    def __init__(self, project, currentTime):
        super().__init__()
        self.project = project
        self.currentTime = currentTime

    def run(self):
        try:
            tmp_dir = "./tmp"
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)

            for file in os.listdir(tmp_dir):
                file_path = os.path.join(tmp_dir, file)
                if os.path.isfile(file_path) and not file.startswith(str(self.currentTime)):
                    os.remove(file_path)

            self.project[0].parse().render_raster(f"{tmp_dir}/{self.currentTime}-bottom.png", dpmm=40)
            self.project[1].parse().render_raster(f"{tmp_dir}/{self.currentTime}-top.png", dpmm=40)
            self.finished.emit(self.currentTime)
            
        except Exception as e:
            QMessageBox.warning(self, '渲染错误', f'渲染错误: {e}', QMessageBox.Yes)