from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox, QPushButton, QLabel, QVBoxLayout, QListWidget, \
    QListWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6 import uic

from domain_types.chapters import Chapter
from ui.widget.topic_widget import TopicWidget


class SectionWidget(QWidget):
    hoursChanged = pyqtSignal()

    # Подсказки IDE
    name_edit: QLineEdit
    semester_combo: QComboBox
    add_topic_btn: QPushButton
    delete_btn: QPushButton
    section_lecture_label: QLabel
    section_practice_label: QLabel
    section_self_study_label: QLabel
    section_sdo_label: QLabel
    section_total_label: QLabel
    topics_container: QVBoxLayout

    def __init__(self, numerator,  controller=None, base_ui_dir='./layout/'):
        super().__init__()
        self.controller = controller
        self.numerator = numerator
        uic.loadUi(base_ui_dir + "section_widget.ui", self)

        self.topics: list[TopicWidget] = []

        # Привязка сигналов
        self.name_edit.textChanged.connect(self.on_hours_changed)
        self.semester_combo.currentIndexChanged.connect(self.on_hours_changed)
        self.add_topic_btn.clicked.connect(self.add_topic)
        self.delete_btn.clicked.connect(self.delete_self)

        # Загрузить список семестров
        self._populate_semesters()

        # Добавить первую тему
        self.add_topic()

    # -----------------------------------------------------------------

    def get_data(self):
        topics = []
        for topic in self.topics:
            topics.append(topic.get_data())

        return Chapter(self.name_edit.text(), int(self.semester_combo.currentText()), topics)



    def _populate_semesters(self):
        self.semester_combo.clear()

        parent = self.parent()
        if parent and hasattr(parent, "get_semester_numbers"):
            nums = parent.get_semester_numbers()
            for n in nums:
                self.semester_combo.addItem(str(n), userData=n)
        else:
            self.semester_combo.addItem("1", userData=1)

    def update_semester_options(self):
        current = self.get_semester()
        self._populate_semesters()

        # Обновление модели списка
        self.semester_combo.model().layoutChanged.emit()

        index = self.semester_combo.findData(current)
        if index != -1:
            self.semester_combo.setCurrentIndex(index)

    # -----------------------------------------------------------------

    def add_topic(self):
        topic = TopicWidget(self.numerator, self)
        topic.hoursChanged.connect(self.on_hours_changed)

        self.topics.append(topic)
        self.topics_container.addWidget(topic)

        self.on_hours_changed()

    def remove_topic(self, topic):
        if topic in self.topics:
            self.topics.remove(topic)
            topic.deleteLater()
            self.on_hours_changed()

    # -----------------------------------------------------------------

    def on_hours_changed(self):
        total_lecture = 0
        total_practice = 0
        total_self_study = 0
        total_sdo = 0

        for topic in self.topics:
            lecture, practice, self_study, sdo = topic.get_hours_by_type()
            total_lecture += lecture
            total_practice += practice
            total_self_study += self_study
            total_sdo += sdo

        total_hours = total_lecture + total_practice + total_self_study

        self.section_lecture_label.setText(f"Лекции: {total_lecture}")
        self.section_practice_label.setText(f"Практики: {total_practice}")
        self.section_self_study_label.setText(f"Сам.раб.: {total_self_study}")
        self.section_sdo_label.setText(f"СДО: {total_sdo}")
        self.section_total_label.setText(f"Всего: {total_hours}")

        self.hoursChanged.emit()

    # -----------------------------------------------------------------

    def delete_self(self):
        if self.controller:
            self.controller.remove_section(self)

    # -----------------------------------------------------------------

    def get_hours_by_type(self):
        total_lecture = 0
        total_practice = 0
        total_self_study = 0
        total_sdo = 0

        for topic in self.topics:
            lecture, practice, self_study, sdo = topic.get_hours_by_type()
            total_lecture += lecture
            total_practice += practice
            total_self_study += self_study
            total_sdo += sdo

        return total_lecture, total_practice, total_self_study, total_sdo

    def get_semester(self):
        data = self.semester_combo.currentData()
        if isinstance(data, int):
            return data
        try:
            return int(self.semester_combo.currentText())
        except Exception:
            return 1
