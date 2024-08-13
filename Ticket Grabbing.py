import sys
import time
import pyautogui
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit

class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Auto Clicker')

        self.layout = QVBoxLayout()

        self.current_time_label = QLabel('Current Time: ', self)
        self.layout.addWidget(self.current_time_label)

        self.target_time_label = QLabel('Set the time for auto-click (HH:MM:SS):', self)
        self.layout.addWidget(self.target_time_label)

        self.time_edit = QLineEdit(self)
        self.layout.addWidget(self.time_edit)

        self.set_time_button = QPushButton('Set Time', self)
        self.set_time_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.set_time_button)

        self.get_position_button = QPushButton('Get Mouse Position', self)
        self.get_position_button.clicked.connect(self.get_mouse_position)
        self.layout.addWidget(self.get_position_button)

        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)

        self.clicks_label = QLabel('Clicks: 0', self)
        self.layout.addWidget(self.clicks_label)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)

        self.time_display_timer = QTimer(self)
        self.time_display_timer.timeout.connect(self.update_current_time)
        self.time_display_timer.start(1000)  # Update every second

        self.target_position = None

    def get_mouse_position(self):
        self.target_position = pyautogui.position()
        self.status_label.setText(f'Target Position: {self.target_position}')

    def start_timer(self):
        self.target_time = QTime.fromString(self.time_edit.text(), 'HH:mm:ss')
        if self.target_time.isValid():
            self.status_label.setText('Timer set for ' + self.target_time.toString('HH:mm:ss'))
            self.timer.start(1000)
        else:
            self.status_label.setText('Invalid time format. Please use HH:MM:SS.')

    def check_time(self):
        current_time = QTime.currentTime()
        if current_time >= self.target_time:
            self.timer.stop()
            self.start_fast_click()

    def start_fast_click(self):
        if self.target_position is None:
            self.status_label.setText('No target position set!')
            return

        self.click_count = 0
        self.fast_click_timer = QTimer(self)
        self.fast_click_timer.timeout.connect(self.perform_click)
        self.fast_click_timer.start(50)  # 50 milliseconds interval, which is 20 clicks per second

    def perform_click(self):
        if self.click_count < 100:
            pyautogui.click(x=self.target_position.x, y=self.target_position.y)
            self.click_count += 1
            self.clicks_label.setText(f'Clicks: {self.click_count}')
        else:
            self.fast_click_timer.stop()
            self.status_label.setText('Finished 100 clicks!')

    def update_current_time(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.current_time_label.setText(f'Current Time: {current_time}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoClickerApp()
    ex.show()
    sys.exit(app.exec_())
