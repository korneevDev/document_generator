from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic

from ui.widget.activity_widget import ActivityWidget


class TopicWidget(QWidget):
    hoursChanged = pyqtSignal()

    name_edit: QLineEdit
    add_activity_btn: QPushButton
    delete_btn: QPushButton
    lecture_label: QLabel
    practice_label: QLabel
    self_study_label: QLabel
    sdo_label: QLabel
    total_label: QLabel
    activities_container: QVBoxLayout

    def __init__(self, parent=None, base_ui_dir='./layout/'):
        super().__init__(parent)

        uic.loadUi(base_ui_dir+"topic_widget.ui", self)

        self.activities: list[ActivityWidget] = []

        # Привязка сигналов
        self.name_edit.textChanged.connect(self.on_hours_changed)
        self.add_activity_btn.clicked.connect(self.add_activity)
        self.delete_btn.clicked.connect(self.delete_self)

        self.add_activity()

    def add_activity(self):
        activity = ActivityWidget(self)
        activity.activityChanged.connect(self.on_hours_changed)

        self.activities.append(activity)
        self.activities_container.addWidget(activity)

        self.on_hours_changed()

    def remove_activity(self, activity: ActivityWidget):
        if activity in self.activities:
            self.activities.remove(activity)
            activity.deleteLater()
            self.on_hours_changed()

    def on_hours_changed(self):
        lecture_hours = 0
        practice_hours = 0
        self_study_hours = 0
        sdo_hours = 0

        for activity in self.activities:
            activity_type = activity.type_combo.currentText()
            hours = activity.hours_spin.value()
            presence = activity.presence_combo.currentText()

            if activity_type == "Лекция":
                lecture_hours += hours
            elif activity_type == "Практика":
                practice_hours += hours
            elif activity_type == "Самостоятельная работа":
                self_study_hours += hours

            if presence == "СДО":
                sdo_hours += hours

        total_hours = lecture_hours + practice_hours + self_study_hours

        self.lecture_label.setText(f"Лекции: {lecture_hours}")
        self.practice_label.setText(f"Практики: {practice_hours}")
        self.self_study_label.setText(f"Сам.раб.: {self_study_hours}")
        self.sdo_label.setText(f"СДО: {sdo_hours}")
        self.total_label.setText(f"Всего: {total_hours}")

        self.hoursChanged.emit()

    def delete_self(self):
        if self.parent() and hasattr(self.parent(), "remove_topic"):
            self.parent().remove_topic(self)

    def get_hours_by_type(self):
        lecture_hours = 0
        practice_hours = 0
        self_study_hours = 0
        sdo_hours = 0

        for activity in self.activities:
            activity_type = activity.type_combo.currentText()
            hours = activity.hours_spin.value()
            presence = activity.presence_combo.currentText()

            if activity_type == "Лекция":
                lecture_hours += hours
            elif activity_type == "Практика":
                practice_hours += hours
            elif activity_type == "Самостоятельная работа":
                self_study_hours += hours

            if presence == "СДО":
                sdo_hours += hours

        return lecture_hours, practice_hours, self_study_hours, sdo_hours
