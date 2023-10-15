import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QPoint, QTimer

WIDTH = 400
HEIGHT = 400
CELL_SIZE = 10

class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle("Snake Game")

        self.score = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move)
        self.timer.start(100)

        self.reset()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw the snake
        painter.setBrush(Qt.green)
        for i in range(len(self.snake)):
            painter.drawRect(self.snake[i].x() * CELL_SIZE, self.snake[i].y() * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        # Draw the food
        painter.setBrush(Qt.red)
        painter.drawRect(self.food.x() * CELL_SIZE, self.food.y() * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        # Draw the score
        painter.drawText(10, 20, "Score: " + str(self.score))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left and self.direction != Qt.Key_Right:
            self.direction = Qt.Key_Left
        elif event.key() == Qt.Key_Right and self.direction != Qt.Key_Left:
            self.direction = Qt.Key_Right
        elif event.key() == Qt.Key_Up and self.direction != Qt.Key_Down:
            self.direction = Qt.Key_Up
        elif event.key() == Qt.Key_Down and self.direction != Qt.Key_Up:
            self.direction = Qt.Key_Down
        else:
            super().keyPressEvent(event)

    def move(self):
        # Move the snake
        head = self.snake[0]
        if self.direction == Qt.Key_Left:
            head = QPoint(head.x() - 1, head.y())
        elif self.direction == Qt.Key_Right:
            head = QPoint(head.x() + 1, head.y())
        elif self.direction == Qt.Key_Up:
            head = QPoint(head.x(), head.y() - 1)
        elif self.direction == Qt.Key_Down:
            head = QPoint(head.x(), head.y() + 1)
        self.snake.insert(0, head)

        # Check for collision with food
        if head == self.food:
            self.score += 1
            self.generateFood()
        else:
            self.snake.pop()

        # Check for collision with walls or self
        if head.x() < 0 or head.x() >= WIDTH / CELL_SIZE or head.y() < 0 or head.y() >= HEIGHT / CELL_SIZE:
            self.gameOver()
        for i in range(1, len(self.snake)):
            if head == self.snake[i]:
                self.gameOver()

        # Redraw the game
        self.update()

    def reset(self):
        # Reset the snake
        self.snake = [QPoint(WIDTH // CELL_SIZE // 2, HEIGHT // CELL_SIZE // 2)]
        self.direction = Qt.Key_Left

        # Generate the first food
        self.generateFood()

        # Reset the score
        self.score = 0

    def generateFood(self):
        while True:
            x = random.randint(0, WIDTH // CELL_SIZE - 1)
            y = random.randint(0, HEIGHT // CELL_SIZE - 1)
            self.food = QPoint(x, y)
            if self.food not in self.snake:
                break

    def gameOver(self):
        self.timer.stop()
        QMessageBox.information(self, "Game Over", "Your score is " + str(self.score))
        self.reset()
        self.timer.start(100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())