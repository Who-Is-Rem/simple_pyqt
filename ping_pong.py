from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PingPong(QWidget):
    def __init__(self): 
        super(PingPong, self).__init__()
        self.ui()
        self.pong_stats()

        self.show()
        
    def ui(self):
        self.score = 0
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setWindowTitle("Ping Pong")
        self.setStyleSheet("background-color:black;")
        
    def pong_stats(self):
        self.px = (self.width()/2)-100
        self.py = self.height()
        self.spd = 50;

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Left:
            self.px -= self.spd
            self.update()
        if k == Qt.Key.Key_Right:
            self.px += self.spd
            self.update()
        
    def keyReleaseEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Left:
            self.update()
        elif k == Qt.Key.Key_Right:
            self.update()

    def paintEvent(self, event):
        print("paint")
        painter = QPainter()
        painter.begin(self)
        self.paint_paddle(painter)
        painter.end()

    def paint_paddle(self, painter): 
        color = QColor(0x808080)
        painter.fillRect(self.px, self.py, 200, 10, color)

    def resizeEvent(self, event):
        self.px = (self.width()/2)-100
        self.py = self.height()-200
        self.update()

if __name__ == "__main__": 
    import sys 
    app = QApplication([])
    pong = PingPong()
    sys.exit(app.exec())







