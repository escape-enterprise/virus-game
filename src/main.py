# Virus Escape Room PC Puzzle
# by Caleb "fivesixfive" North

# Constants
RESOLUTION = (1920, 1080)

# Imports
from sys import argv
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import \
    QApplication, QWidget, QMainWindow, \
    QVBoxLayout, QHBoxLayout, \
    QLineEdit, QLabel

# Build Window
def main():
    q = QApplication(argv)
    q.setApplicationDisplayName("Virus Game")
    # Setup Window
    main_window = QMainWindow()
    main_window.setWindowTitle("Virus Game")
    main_window.showFullScreen()
    main_window.setCursor(Qt.BlankCursor)
    # Setup Window Layout
    main_layout = QVBoxLayout()
    main_window.setLayout(main_layout)
    # Title Layout
    # Countdown Layout
    # Start Event Loop
    q.exec_()

# Execute
if __name__ == "__main__":
    main()
