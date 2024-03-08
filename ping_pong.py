from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class PingPong(QMainWindow):
    def __init__(self):
        super(PingPong, self).__init__()
 
        self.board = Board(self)

        self.setCentralWidget(self.board)
        self.board.start()

        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setWindowTitle("Ping Pong")

class Board(QFrame):
    def __init__(self, parent): 
        super(Board, self).__init__(parent)

        self.timer = QBasicTimer()
        
        # Have directions 0,1: left or right  
        self.direction = 0
        self.dx = (self.contentsRect().width()/2)-50

        # Board parameters 
        self.rec = self.contentsRect()
        self.maxx = self.rec.width()
        self.maxy = self.rec.height()

    def start(self):
        self.timer.start(50, self)

    def paint(self, event): 
        # make painter 
        painter = QPainter(self)

        self.draw_paddle(painter, (self.maxx/2)-50, self.rec.bottom()+100)


    def draw_paddle(self, painter, x, y): 
        #color 
        color = QColor(0x808080)
        painter.fillRect(x, y, 100, 5, color)
        
    def key_press(self, event): 
        key = event.key()

        if key == Qt.Key.Key_Left:
            self.direction = 0 
        elif key == Qt.Key.Key_Right:
            self.direction = 1
        else:
            self.direction = 2

    def move_paddle(self): 
        if self.direction == 0:
            if self.dx <= 0:
                self.dx = 0
            else: 
                self.dx -= 10 
        elif self.direction == 1: 
            if self.dx >= self.maxx:
                self.dx = 0
            else:
                self.dx += 10
        elif self.direction == 2:
            pass

    def timerEvent(self, event): 
        if event.timerId() == self.timer.timerId():
            self.move_paddle()
            self.update()
            

        



if __name__ == "__main__": 
    import sys 
    app = QApplication([])
    pong = PingPong()
    pong.show()
    sys.exit(app.exec())







