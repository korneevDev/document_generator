from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic


class ActivityWidget(QWidget):
    activityChanged = pyqtSignal()

    name_edit: QLineEdit
    type_combo: QComboBox
    hours_spin: QSpinBox
    presence_combo: QComboBox
    delete_btn: QPushButton

    def __init__(self, parent=None, base_ui_dir='./layout/'):
        super().__init__(parent)

        uic.loadUi(base_ui_dir + "activity_widget.ui", self)

        self.name_edit.textChanged.connect(self.on_activity_changed)
        self.type_combo.currentTextChanged.connect(self.on_activity_changed)
        self.hours_spin.valueChanged.connect(self.on_activity_changed)
        self.presence_combo.currentTextChanged.connect(self.on_activity_changed)
        self.delete_btn.clicked.connect(self.delete_self)

    def on_activity_changed(self):
        if self.type_combo.currentText() == 'Самостоятельная работа':
            self.presence_combo.setCurrentIndex(2)
            self.presence_combo.setEnabled(False)
        else:
            if self.presence_combo.currentIndex() == 2:
                self.presence_combo.setCurrentIndex(0)
            self.presence_combo.setEnabled(True)

        self.activityChanged.emit()

    def delete_self(self):
        if self.parent() and hasattr(self.parent(), "remove_activity"):
            self.parent().remove_activity(self)
