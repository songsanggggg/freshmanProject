from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

# 加载中窗口
class LoadingWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('加载中...')
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setModal(True)
        self.setFixedSize(220, 150)
        layout = QVBoxLayout()
        
        self.movie = QMovie('./resource/loading.gif')
        self.movie.setScaledSize(QSize(200, 200))
        self.loadingGif = QLabel()
        self.loadingGif.setMovie(self.movie)
        layout.addWidget(self.loadingGif)
        
        self.setLayout(layout)
        self.movie.start()