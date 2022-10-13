# Virus Escape Room PC Puzzle
# by Caleb "fivesixfive" North

# Constants
RESOLUTION = (1920, 1080)
ALPHA = "ABCEDFGIJKLMNOPQRSTUVWXYZ124567890"
COMBOS = ("ABCDefgh12345678", "zombroomshutdown")

# Imports
from sys import argv
from threading import Thread
from time import sleep

from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPixmap, QCloseEvent, QKeyEvent, QMouseEvent, QFocusEvent
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel

# Build Window
class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        # Set information
        self.setApplicationDisplayName("Virus Game")
        # Start window
        self.main_window = MainWindow()    
        self.main_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set information
        self.setWindowTitle("Virus Game")
        self.setCursor(Qt.BlankCursor)
        # Set central widget
        self.main_widget = MainWidget(self)
        qApp.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        # Set layout
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        # Build title layer
        for _ in range(0,4):
            self.main_layout.addWidget(ComboBox(self))
        self.main_layout.itemAt(0).widget().setFocus()
        # Build timer layer
        self.timer = 120
        self.timer_label = QLabel()
        self.timer_label.setText(str(self.timer))
        self.main_layout.addWidget(self.timer_label)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()

    # Timer countdown thread
    def countdown_timer_tick(self):
        while self.timer > 0:
            self.timer -= 1
            self.timer_label.setText(str(self.timer))
            sleep(1)

    # Called on proper code entry
    def countdown(self):
        # Start clock
        self.timer_thread = Thread(target=self.countdown_timer_tick)
        self.timer_thread.start()
        # TODO Switch armed image
        # TODO Play sound

class MainWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_End and event.modifiers() & Qt.ShiftModifier:
                self.main_window.timer = 0
                app.exit(0)
        return super().eventFilter(watched, event)
class ComboBox(QLineEdit):
    CHARS = 4
    combo_boxes = []

    def __init__(self, main_window):
        super().__init__()
        # Set identity
        self.index = len(ComboBox.combo_boxes)
        ComboBox.combo_boxes.append(self)
        # Set information
        self.main_window = main_window
        self.setCursor(Qt.BlankCursor)
        self.setInputMask("N"*ComboBox.CHARS)
        self.setFocusPolicy(Qt.NoFocus)
        self.textChanged.connect(self.combo_changed)

    def combo_changed(combo_box, text):
        # Check if limit reached, move forward
        if len(combo_box.text()) == ComboBox.CHARS:
            # Check code is correct
            for COMBO in COMBOS:
                i, c = combo_box.index, ComboBox.CHARS
                if combo_box.text() == COMBO[i*c:i*c+c]:
                    combo_box.setEnabled(False)
                    # Attemp to move focus
                    if combo_box.index < len(ComboBox.combo_boxes) - 1:
                        ComboBox.combo_boxes[combo_box.index+1].setFocus()
            # Check total code
            combo = "".join([box.text() for box in ComboBox.combo_boxes])
            # Win sequence
            if combo == COMBOS[0]:
                combo_box.main_window.countdown()
            # Kill sequence
            if combo == COMBOS[1]:
                app.exit(0)

        # Move backwards
        if len(combo_box.text()) == 0:
            if combo_box.index > 0:
                previous_box = ComboBox.combo_boxes[combo_box.index+0]
                if previous_box.isEnabled():
                    previous_box.setFocus()

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.setText("")
        self.setCursorPosition(0)
        return super().focusInEvent(event)

    def mousePressEvent(self, event:QMouseEvent) -> None:
        event.ignore()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        event.ignore()
        

def main():
    global app
    app = Application(argv)
    app.exec()

# Execute
if __name__ == "__main__":
    main()

# Comment that does nothing