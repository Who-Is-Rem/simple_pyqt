from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

"""
Class for the main window for the Ping Pong Game
"""
class PingPong(QMainWindow):
    def __init__(self):
        super().__init__()
        # initialize window data
        self.setWindowTitle("Ping Pong")
        self.setMaximumSize(1440, 900)
        self.setFixedSize(1440, 900)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.grabMouse()

        # timer for modifying update() rate
        self.timer = QBasicTimer()
        self.timer.start(20, self)

        # make the board 
        self.board = Board(self, 5,5)
        self.board.make_layout()
        self.setCentralWidget(self.board)

        # initialize the player 
        self.player = Player(self)
        self.p_height = self.height()-150
        self.player.move(int((self.width()/2)-(self.player.width()/2)), self.p_height)

        self.show()

    """
    Event to track mouse movement and connect it to the player
    """
    def mouseMoveEvent(self, event):
        pos_x = int(event.position().x())-int(self.player.width()/2)
        self.player.move(pos_x, self.p_height)

"""
Class for making objects that can collide
"""
class Collision(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

    def collision(self, other:QWidget): 
        dim = self.contentsRect()
        other_dim = other.contentsRect()
        if other.x() < dim.x() | (dim.x()+dim.width()) < (other.x()+other_dim.width()):
            if other.y() < dim.y() | (dim.y()+dim.height()) < (other.y()+other_dim.height()):
                return True
        return False

"""
Class containing the main board of the game which has the collision objects and borders
"""
class Board(QFrame):
    def __init__(self, parent, rows, cols):
        super().__init__(parent)
        self.side = 25
        self.rows = rows
        self.cols = cols
        self.objects = []

    """
    Makes the layout for where the borders and target objects should be 
    """
    def make_layout(self):
        layout = QGridLayout()

        # The blocks to be broken 
        layout.addLayout(self.make_grid(), 1, 1, Qt.AlignmentFlag.AlignCenter)
        
        # the borders of the "map"
        layout.addWidget(Bounds(self, "horizontal"), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(Bounds(self, "vertical"), 0, 0, 3, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(Bounds(self, "vertical"), 0, 2, 3, 1, Qt.AlignmentFlag.AlignTop)

        # set the layout 
        self.setLayout(layout)

    """
    Makes a square grid of targets to hit 
    """
    def make_grid(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(1)
        layout.setHorizontalSpacing(1)
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                sq = Target(self, self.side)
                row.append(sq)
                layout.addWidget(sq, i, j, 1, 1)
            self.objects.append(row)
        return layout

    """
    Makes one side of the border
    """
    def make_edge(self, orient):
        return Bounds(self, orient)

"""
Class representing the targets to be shot at 
"""
class Target(Collision):
    def __init__(self, parent, side):
        super().__init__(parent)
        self.side = side
        self.setFixedSize(self.side, self.side)
        self.setStyleSheet("background-color:red")

"""
Class representing the boundaries for the game 
"""
class Bounds(Collision):
    def __init__(self, parent, orient:str):
        super().__init__(parent)
        if orient != "vertical" and orient != "horizontal": print(f"Orientation: {orient}. Bad Arg") 
        if orient == "vertical":
            self.setFixedSize(10, int(parent.parentWidget().maximumHeight()*(5/6)))
            self.setStyleSheet("background-color:blue")
        elif orient == "horizontal":
            self.setFixedSize(int(parent.parentWidget().maximumWidth()-20), 10)
            self.setStyleSheet("background-color:green")

"""
Class representing the player, i.e. the paddle
"""
class Player(Collision):
    def __init__(self, parent): 
        super().__init__(parent)
        self.setFixedSize(250, 10)
        self.setStyleSheet("background-color:grey;")
        self.px = 0
        self.py = 0

if __name__ == "__main__":
    app = QApplication()
    pong = PingPong()
    app.exec()
