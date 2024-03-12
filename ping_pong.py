from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import math

"""
Class for the main window for the Ping Pong Game
"""
class PingPong(QMainWindow):
    def __init__(self, cols, rows):
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
        self.timer.start(10, self)

        # make the board 
        self.board = Board(self, cols, rows)
        self.board.make_layout()
        self.setCentralWidget(self.board)

        # initialize the player 
        self.player = Player(self)
        self.p_height = self.height()-150
        self.player.move(int((self.width()/2)-(self.player.width()/2)), self.p_height)

        # initialize bullet 
        self.init_bullet = Bullet(self)
        self.bullet_shot = False
        self.init_bullet.move(int(self.width()/2), self.p_height-int(self.init_bullet.height())-1)
        self.bullets = []

        self.show()

    """
    Event to increase update speed and detect collisions 
    """
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId(): 
            for b in self.bullets:
                # move the bullets 
                nx = b.x() + b.xspd
                ny = b.y() + b.yspd
                b.move(nx, ny)

                # check for collision and adjust velocity accordingly 
                self.bullet_collision(b)

    """
    Helper method to change bullet speed according to collisions 
    """
    def bullet_collision(self, bullet):
        # check for collision with vertical border 
        if bullet.collision(self.board.left):
            bullet.rev_x()
        if bullet.collision(self.board.right): 
            bullet.rev_x()
        # check for collision with top border
        elif bullet.collision(self.board.top):
            bullet.rev_y()
        # check for collision with player 
        elif bullet.collision(self.player):
            # reverse y spd of the bullet 
            bullet.rev_y()
            # adjust x spd of the bullet dependent of the location hit on the player
            angle = self.player_bullet(bullet)
            dx = bullet.dx * (math.sin(angle))
            bullet.xspd = dx

        # check for collision with obstacles and delete them and adjust bullet accordingly 
        hit = False
        for i in range(len(self.board.objects)):
            row = self.board.objects[i]
            for o in row[::1]:
                if bullet.collision(o):
                    hit = True
                    row.remove(o)
                    o.hide()
        if hit: bullet.rev_y(); bullet.rev_x()

    """
    Helper method to get the relative angle the bullet should bounce off the player 
    """
    def player_bullet(self, bullet):
        b_x = bullet.x() + (bullet.width()/2)
        p_center = self.player.x()+(self.player.width()/2)
        rel_x = b_x - p_center
        ratio = rel_x/(self.player.width()/2)
        return ratio*(math.pi/2)

    """
    Event to track mouse movement and connect it to the player
    """
    def mouseMoveEvent(self, event):
        pos_x = int(event.position().x())-int(self.player.width()/2)
        self.player.move(pos_x, self.p_height)
        if not self.bullet_shot: 
            self.init_bullet.move(pos_x+int(self.player.width()/2), self.p_height-int(self.init_bullet.height())-1)

    """
    Event to detect space presses and initialize the game by shooting the bullet 
    """
    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Space and not self.bullet_shot: 
            self.bullet_shot = True 
            self.init_bullet.yspd = -self.init_bullet.dy 
            self.bullets.append(self.init_bullet)

"""
Class for making objects that can collide
"""
class Bullet(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.yspd = 0
        self.xspd = 0
        self.dy = 5
        self.dx = 5

    """
    Reverse the speed of the bullet in the x direction 
    """
    def rev_x(self):
        self.xspd = -self.xspd 

    """
    Reverse the speed of the bullet in the y direction 
    """
    def rev_y(self): 
        self.yspd = -self.yspd

    """
    Check for collisions between the bullet and some other widget 
    """
    def collision(self, other:QWidget): 
        if ((other.x()-3 < self.x() < other.x()+other.width()+3) or 
            (other.x()-3 < self.x()+self.width() < other.x()+other.width()+3)):
            if ((other.y()-3 < self.y() < other.y()+other.height()+3) or 
                (other.y()-3 < self.y()+self.height() < other.y()+other.height()+3)):
                return True
        return False

    """
    Paints a circular bullet that fills the frame
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        circle_path = QPainterPath()
        circle_path.addEllipse(self.contentsRect())
        painter.fillPath(circle_path, QColor(0x0000FF))
        painter.end()

"""
Class containing the main board of the game which has the collision objects and borders
"""
class Board(QFrame):
    def __init__(self, parent, cols, rows):
        super().__init__(parent)
        assert cols <= 45
        assert rows <= 20
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
        self.top = Bounds(self, "horizontal")
        self.left = Bounds(self,  "vertical")
        self.right = Bounds(self, "vertical")
        layout.addWidget(self.top, 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.left, 0, 0, 5, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.right, 0, 2, 5, 1, Qt.AlignmentFlag.AlignTop)

        # set the layout 
        self.setLayout(layout)

    """
    Makes a square grid of targets to hit 
    """
    def make_grid(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        for i in range(self.rows):
            layout.setRowMinimumHeight(i, self.side+2)
            row = []
            for j in range(self.cols):
                layout.setColumnMinimumWidth(j, self.side+2)
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
class Target(QFrame):
    def __init__(self, parent, side):
        super().__init__(parent)
        self.side = side
        self.setFixedSize(self.side, self.side)
        self.setStyleSheet("background-color:red")

"""
Class representing the boundaries for the game 
"""
class Bounds(QFrame):
    def __init__(self, parent, orient:str):
        super().__init__(parent)
        if orient != "vertical" and orient != "horizontal": print(f"Orientation: {orient}. Bad Arg") 
        if orient == "vertical":
            self.setFixedSize(10, int(parent.parentWidget().maximumHeight()*(7/8)))
        elif orient == "horizontal":
            self.setFixedSize(int(parent.parentWidget().maximumWidth()-30), 10)
        self.setStyleSheet("background-color:grey")

"""
Class representing the player, i.e. the paddle
"""
class Player(QFrame):
    def __init__(self, parent): 
        super().__init__(parent)
        self.setFixedSize(250, 10)
        self.setStyleSheet("background-color:grey;")
        self.px = 0
        self.py = 0

if __name__ == "__main__":
    app = QApplication()
    pong = PingPong(45, 20)
    app.exec()
