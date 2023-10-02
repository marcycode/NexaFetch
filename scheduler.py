from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QTimeEdit, QPushButton, QComboBox
from PyQt5.QtCore import QTimer, QDateTime

class Scheduler(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        self.time_picker = QTimeEdit(self)
        layout.addWidget(self.time_picker)

        self.frequency_dropdown = QComboBox(self)
        self.frequency_dropdown.addItems(["Once Daily", "Once Weekly"])
        layout.addWidget(self.frequency_dropdown)

        self.set_schedule_button = QPushButton('Set Schedule', self)
        self.set_schedule_button.clicked.connect(self.schedule_task)
        layout.addWidget(self.set_schedule_button)

        self.setLayout(layout)

    def schedule_task(self):
        current_datetime = QDateTime.currentDateTime()
        selected_date = self.calendar.selectedDate()
        selected_time = self.time_picker.time()

        scheduled_datetime = QDateTime(selected_date, selected_time)
        if scheduled_datetime < current_datetime:
            scheduled_datetime = self.add_time_based_on_frequency(scheduled_datetime)

        interval = current_datetime.msecsTo(scheduled_datetime)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.callback)
        self.timer.timeout.connect(self.schedule_task)  # Reschedule after task completion
        self.timer.start(interval)

    def add_time_based_on_frequency(self, datetime):
        frequency = self.frequency_dropdown.currentText()
        if frequency == "Once Daily":
            return datetime.addDays(1)
        elif frequency == "Once Weekly":
            return datetime.addDays(7)
        else:
            return datetime  # Fallback to the original datetime
