from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

"""
Class for the main window for the Ping Pong Game
"""
class PingPong(QMainWindow):
    def __init__(self, num_players=0):
        super().__init__()
        assert num_players >=0 and num_players < 3
        self.num_players = num_players

        # initialize window data
        self.setWindowTitle("Ping Pong")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setStyleSheet("background-color:black;")

        # timer for modifying update() rate
        self.timer = QBasicTimer()
        self.timer.start(20, self)

        # set of keys to know what keys have been pressed
        self.keys = set()

        # initialize the players
        self.initPlayer()

        self.show()

    """
    initialize the players' data such as position, key presses, and the players themself
    """
    def initPlayer(self):
        self.players = []
        player_ypos = [self.height()-150, 150]
        player_xpos = (self.width()/2)-100
        player_keys = [(Qt.Key.Key_Left, Qt.Key.Key_Right), (Qt.Key.Key_A, Qt.Key.Key_D)]
        for i in range(self.num_players):
            self.players.append(Player(player_xpos, player_ypos[i], player_keys[i][0], player_keys[i][1]))

    """
    Event to paint the players on the main window whenever update() gets triggered
    """
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for p in self.players:
            painter.fillRect(p.px, p.py, p.width, p.height, QColor(0x808080))
        painter.end()

    """
    Event to increase the speed of update triggering with a timer
    """
    def timerEvent(self, event):
        print(self.keys)
        if event.timerId() == self.timer.timerId():
            for p in self.players:
                # decelerate for existing players if no key is pressed for respective player
                if not (p.left in self.keys or p.right in self.keys) and abs(p.speed) > 0:
                    p.accelerate(0)
                # update player speeds
                p.px += p.speed
            self.update()


    """
    Detect key presses and modify the players' speeds accordingly
    """
    def keyPressEvent(self, event):
        self.keys.add(event.key())
        for p in self.players:
            if not p.left & p.right in self.keys:
                # accelerate left 
                if p.left in self.keys:
                    p.accelerate(-1)
                # accelerate right 
                if p.right in self.keys:
                    p.accelerate(1)

    """
    Detect key releases and decrease the players' speeds if neither of the respective keys for
    the players are pressed
    """
    def keyReleaseEvent(self, event):
        try:
            self.keys.remove(event.key())
        except: pass

    """
    Change the player position when the window resets in size
    """
    def resizeEvent(self, event):
        player_xpos = (self.width()/2)-100
        for p in self.players:
            p.px = player_xpos
        if self.players[0] != 0:
            self.players[0].py = self.height()-150


"""
Class for players i.e. the paddles in the game
"""
class Player():
    def __init__(self, x, y, left:Qt.Key, right:Qt.Key):
        # data for positions
        self.direction = 2
        self.px = x
        self.py = y

        # data for size
        self.width = 250
        self.height = 10

        # data for speed
        self.speed = 0
        self.max_spd = 40
        self.acceleration = 10

        # movement keys
        self.left = int(left)
        self.right = int(right)

    """
    Modifies speed and position according to the direction of acceleration
    described by num

    num:
    0 - decelerate
    1 - accelerate in the +x
    -1 - accelerate in the -x
    """
    def accelerate(self, num=0):
        # accelerate
        if abs(self.speed) < self.max_spd:
            if num == 1:
                self.speed += self.acceleration
            elif num == -1:
                self.speed -= self.acceleration
        # decelerate
        if num == 0:
            if self.speed != 0:
                tsp = abs(self.speed) - self.acceleration
                if self.speed < 0:
                    self.speed = -tsp
                else:
                    self.speed = tsp
            elif abs(self.speed) < 5:
                self.speed = 0

if __name__ == "__main__":
    app = QApplication()
    pong = PingPong(1)
    app.exec()
