from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PingPong(QWidget):
    def __init__(self): 
        super(PingPong, self).__init__()
        self.timer = QBasicTimer()
        self.ui()
        self.pong_stats()

        self.start()
        self.show()
        
    def ui(self):
        self.score = 0
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setWindowTitle("Ping Pong")
        self.setStyleSheet("background-color:black;")
        
    def pong_stats(self):
        self.px = (self.width()/2)-100
        self.dx = 0
        self.refresh = 50

    def start(self):
        self.timer.start(self.refresh, self)

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Left:
            self.dx = -50
        if k == Qt.Key.Key_Right:
            self.dx = 50
        
    def keyReleaseEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Left or k == Qt.Key.Key_Right:
            self.dx = 0

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.paint_paddle(painter)
        painter.end()

    def paint_paddle(self, painter): 
        color = QColor(0x808080)
        self.px += self.dx
        painter.fillRect(self.px, self.height()-200, 200, 10, color)

    def resizeEvent(self, event):
        self.px = (self.width()/2)-100
        self.update()

if __name__ == "__main__": 
    import sys 
    app = QApplication([])
    pong = PingPong()
    sys.exit(app.exec())







