# Virus Escape Room PC Puzzle
# by Caleb "fivesixfive" North

# Constants
RESOLUTION = (1920, 1080)
ALPHA = "ABCEDFGHIJKLMNOPQRSTUVWXYZ124567890Backspace"
COMBOS = ("ABCDefgh12345678", "zombroomshutdown")

# Imports
from sys import argv
from threading import Thread
from time import sleep

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Build Window
class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        # Set information
        self.setApplicationDisplayName("Virus Game")
        # Load appearance
        #QFontDatabase.addApplicationFont("../font/DIGITALDREAMSKEWNARROW.ttf")
        print(QFontDatabase.applicationFontFamilies(0))
        with open("main.qss","r") as qss:
            self.setStyleSheet(qss.read())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set information
        self.setWindowTitle("Virus Game")
        self.setCursor(Qt.BlankCursor)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Set central widget
        self.main_widget = MainWidget(self)
        app.installEventFilter(self.main_widget)
        self.setCentralWidget(self.main_widget)
        # Set layout
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        # Build title layer
        self.title = Title()
        self.title.setText("Self Destruct\nControl Panel")
        self.main_layout.addWidget(self.title)
        # Build combo layer
        self.combo_layout = QHBoxLayout()
        self.main_layout.addLayout(self.combo_layout)
        for _ in range(0,4):
            self.combo_layout.addWidget(ComboBox(self))
        self.combo_layout.itemAt(0).widget().setVisible(True)
        self.combo_layout.itemAt(0).widget().setFocus()
        # Build timer layer
        self.timer = 120
        self.timer_label = TimerLabel()
        self.timer_label.setText("2:00")
        self.main_layout.addWidget(self.timer_label)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()

    # Timer countdown thread
    def countdown_timer_tick(self):
        while self.timer > 0:
            timer_text = f"{int((self.timer/60))}:{self.timer % 60}"
            self.timer_label.setText(timer_text)
            self.timer -= 1
            sleep(1)

    def combo_changed(index):
        pass

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

class Title(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)

class ComboBox(QLineEdit):
    CHARS = 4
    combo_boxes = []

    def __init__(self, main_window):
        super().__init__()
        # Set identity
        self.index = len(ComboBox.combo_boxes)
        ComboBox.combo_boxes.append(self)
        self.setVisible(False)
        # Set information
        self.main_window = main_window
        self.setCursor(Qt.BlankCursor)
        self.setMaxLength(4)
        self.setFocusPolicy(Qt.NoFocus)
        # Set display
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        #if QKeySequence(event.keyCombination()).toString() in ALPHA:
         # Attemp to move focus
        if event.key() & Qt.Key_Enter:
            # Check if limit reached, move forward
            if len(self.text()) == ComboBox.CHARS:
                # Check code is correct
                for COMBO in COMBOS:
                    i, c = self.index, ComboBox.CHARS
                    if self.text() == COMBO[i*c:i*c+c]:
                        self.setEnabled(False)
                        if self.index < len(ComboBox.combo_boxes) - 1:
                            ComboBox.combo_boxes[self.index+1].setVisible(True)
                            ComboBox.combo_boxes[self.index+1].setFocus()
                            ComboBox.combo_boxes[self.index].setVisible(False)
                    # Check total code
                    combo = "".join([box.text() for box in ComboBox.combo_boxes])
                    self.main_window.combo_changed(self.index)
                    # Kill sequence
                    if combo == COMBOS[1]:
                        app.exit(0)
        return super().keyPressEvent(event)
        #event.ignore()

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.setText("")
        self.setCursorPosition(0)
        return super().focusInEvent(event)

    def mousePressEvent(self, event:QMouseEvent) -> None:
        event.ignore()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        event.ignore()
        
class TimerLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)

def main():
    global app
    app = Application(argv)
    main_window = MainWindow()    
    main_window.showFullScreen()
    #main_window.show()
    app.exec()

# Execute
if __name__ == "__main__":
    main()

# Comment that does nothing