
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.time = 0  # Waktu dalam detik
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.label = QLabel("0", self)
        self.start_btn = QPushButton("Start", self)
        self.pause_btn = QPushButton("Pause", self)
        self.reset_btn = QPushButton("Reset", self)

        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)

    def update_timer(self):
        self.time += 1
        self.label.setText(str(self.time))

    def start_timer(self):
        self.timer.start(1000)  # Update setiap 1 detik

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.time = 0
        self.label.setText("0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec_())