import multiprocessing
multiprocessing.freeze_support()
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QApplication, QWidget
import warnings
warnings.filterwarnings("ignore")
from PyQt5.QtCore import Qt

class jendelaloading(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.movie = QMovie('load.gif')
        self.label.setMovie(self.movie)
        self.movie.start()
        self.setGeometry(1000, 500, 150, 150)
        self.setMinimumSize(150, 150)
        self.resize(150, 150)
        self.setMaximumSize(150, 150)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
"""
if __name__ == '__main__':
    app = QApplication([])
    widget = jendelaloading()
    widget.show()
    app.exec_()
"""