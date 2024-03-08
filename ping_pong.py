from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PingPong(QWidget):
    def __init__(self): 
        super(PingPong, self).__init__()
        self.ui()
        
    def ui(self):
        self.score = 0
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setWindowTitle("Ping Pong")

        rec = self.rect()
        self.maxw = rec.width()
        self.maxh = rec.height()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Left:
            print("left")
        if k == Qt.Key.Key_Right:
            print("right")
        
    def keyReleaseEvent(self, event):
        print("released")

    def paintEvent(self, event):
        pass 

    def paint_paddle(self, painter): 
        pass 


if __name__ == "__main__": 
    import sys 
    app = QApplication([])
    pong = PingPong()
    sys.exit(app.exec())







