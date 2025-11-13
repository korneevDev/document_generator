import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal


class ActivityWidget(QWidget):
    # Сигнал об изменении занятия
    activityChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        # Название занятия
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название занятия")
        self.name_edit.textChanged.connect(self.on_activity_changed)

        # Вид деятельности
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Лекция", "Практика", "Самостоятельная работа"])
        self.type_combo.currentTextChanged.connect(self.on_activity_changed)

        # Часы
        self.hours_spin = QSpinBox()
        self.hours_spin.setMaximum(1000)
        self.hours_spin.valueChanged.connect(self.on_activity_changed)

        # Форма присутствия
        self.presence_combo = QComboBox()
        self.presence_combo.addItems(["Очно", "СДО"])
        self.presence_combo.currentTextChanged.connect(self.on_activity_changed)

        # Кнопка удаления
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_self)

        self.layout.addWidget(QLabel("Название:"))
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(QLabel("Вид:"))
        self.layout.addWidget(self.type_combo)
        self.layout.addWidget(QLabel("Часы:"))
        self.layout.addWidget(self.hours_spin)
        self.layout.addWidget(QLabel("Форма:"))
        self.layout.addWidget(self.presence_combo)
        self.layout.addWidget(self.delete_btn)

    def on_activity_changed(self):
        # Отправляем сигнал наверх
        self.activityChanged.emit()

    def delete_self(self):
        if self.parent():
            self.parent().remove_activity(self)


class TopicWidget(QWidget):
    # Сигнал об изменении часов
    hoursChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.activities = []

        # Заголовок темы
        header_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название темы")
        self.name_edit.textChanged.connect(self.on_hours_changed)

        self.add_activity_btn = QPushButton("+ Добавить занятие")
        self.add_activity_btn.clicked.connect(self.add_activity)

        self.delete_btn = QPushButton("Удалить тему")
        self.delete_btn.clicked.connect(self.delete_self)

        header_layout.addWidget(QLabel("Тема:"))
        header_layout.addWidget(self.name_edit)
        header_layout.addWidget(self.add_activity_btn)
        header_layout.addWidget(self.delete_btn)
        header_layout.addStretch()

        self.layout.addLayout(header_layout)

        # Сводка по часам
        self.hours_summary_layout = QHBoxLayout()
        self.lecture_label = QLabel("Лекции: 0")
        self.practice_label = QLabel("Практики: 0")
        self.self_study_label = QLabel("Сам.раб.: 0")
        self.sdo_label = QLabel("СДО: 0")
        self.total_label = QLabel("Всего: 0")

        self.hours_summary_layout.addWidget(self.lecture_label)
        self.hours_summary_layout.addWidget(self.practice_label)
        self.hours_summary_layout.addWidget(self.self_study_label)
        self.hours_summary_layout.addWidget(self.sdo_label)
        self.hours_summary_layout.addWidget(self.total_label)
        self.hours_summary_layout.addStretch()

        self.layout.addLayout(self.hours_summary_layout)

        # Контейнер для занятий
        self.activities_container = QVBoxLayout()
        self.layout.addLayout(self.activities_container)

        self.add_activity()  # Добавляем первое занятие по умолчанию

    def add_activity(self):
        activity = ActivityWidget(self)
        activity.activityChanged.connect(self.on_hours_changed)
        self.activities.append(activity)
        self.activities_container.addWidget(activity)
        self.on_hours_changed()

    def remove_activity(self, activity):
        self.activities.remove(activity)
        activity.deleteLater()
        self.on_hours_changed()

    def on_hours_changed(self):
        # Пересчитываем суммарные часы по типам занятий
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

        # Обновляем сводку
        self.lecture_label.setText(f"Лекции: {lecture_hours}")
        self.practice_label.setText(f"Практики: {practice_hours}")
        self.self_study_label.setText(f"Сам.раб.: {self_study_hours}")
        self.sdo_label.setText(f"СДО: {sdo_hours}")
        self.total_label.setText(f"Всего: {total_hours}")

        # Отправляем сигнал наверх
        self.hoursChanged.emit()

    def delete_self(self):
        if self.parent():
            self.parent().remove_topic(self)

    def get_hours_by_type(self):
        """Возвращает часы по типам занятий"""
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


class SectionWidget(QWidget):
    # Сигнал об изменении часов
    hoursChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.topics = []

        # Заголовок раздела
        self.header_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название раздела")
        self.name_edit.textChanged.connect(self.on_hours_changed)

        # Семестр для раздела
        self.semester_spin = QSpinBox()
        self.semester_spin.setRange(1, 12)
        self.semester_spin.setValue(1)
        self.semester_spin.valueChanged.connect(self.on_hours_changed)

        self.add_topic_btn = QPushButton("+ Добавить тему")
        self.add_topic_btn.clicked.connect(self.add_topic)
        self.delete_btn = QPushButton("Удалить раздел")
        self.delete_btn.clicked.connect(self.delete_self)

        self.header_layout.addWidget(QLabel("Раздел:"))
        self.header_layout.addWidget(self.name_edit)
        self.header_layout.addWidget(QLabel("Семестр:"))
        self.header_layout.addWidget(self.semester_spin)
        self.header_layout.addWidget(self.add_topic_btn)
        self.header_layout.addWidget(self.delete_btn)
        self.header_layout.addStretch()

        self.layout.addLayout(self.header_layout)

        # Сводка по часам раздела
        self.section_summary_layout = QHBoxLayout()
        self.section_lecture_label = QLabel("Лекции: 0")
        self.section_practice_label = QLabel("Практики: 0")
        self.section_self_study_label = QLabel("Сам.раб.: 0")
        self.section_sdo_label = QLabel("СДО: 0")
        self.section_total_label = QLabel("Всего: 0")

        # Подсветка при превышении часов
        self.section_total_label.setStyleSheet("font-weight: bold;")

        self.section_summary_layout.addWidget(QLabel("Раздел:"))
        self.section_summary_layout.addWidget(self.section_lecture_label)
        self.section_summary_layout.addWidget(self.section_practice_label)
        self.section_summary_layout.addWidget(self.section_self_study_label)
        self.section_summary_layout.addWidget(self.section_sdo_label)
        self.section_summary_layout.addWidget(self.section_total_label)
        self.section_summary_layout.addStretch()

        self.layout.addLayout(self.section_summary_layout)

        # Контейнер для тем
        self.topics_container = QVBoxLayout()
        self.layout.addLayout(self.topics_container)

        self.add_topic()  # Добавляем первую тему по умолчанию

    def add_topic(self):
        topic = TopicWidget(self)
        topic.hoursChanged.connect(self.on_hours_changed)
        self.topics.append(topic)
        self.topics_container.addWidget(topic)
        self.on_hours_changed()

    def remove_topic(self, topic):
        self.topics.remove(topic)
        topic.deleteLater()
        self.on_hours_changed()

    def on_hours_changed(self):
        # Пересчитываем суммарные часы по разделу
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

        # Обновляем сводку раздела
        self.section_lecture_label.setText(f"Лекции: {total_lecture}")
        self.section_practice_label.setText(f"Практики: {total_practice}")
        self.section_self_study_label.setText(f"Сам.раб.: {total_self_study}")
        self.section_sdo_label.setText(f"СДО: {total_sdo}")
        self.section_total_label.setText(f"Всего: {total_hours}")

        # Передаем сигнал дальше наверх
        self.hoursChanged.emit()

    def delete_self(self):
        if self.parent():
            self.parent().remove_section(self)

    def get_hours_by_type(self):
        """Возвращает часы по типам занятий для всего раздела"""
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
        """Возвращает номер семестра раздела"""
        return self.semester_spin.value()


class SemesterSummaryWidget(QWidget):
    """Виджет для отображения сводки по одному семестру"""

    def __init__(self, semester_number, parent=None):
        super().__init__(parent)
        self.semester_number = semester_number
        self.layout = QHBoxLayout(self)

        self.status_label = QLabel(f"Семестр {semester_number}:")
        self.details_label = QLabel("Лекции: 0, Практики: 0, Сам.раб.: 0, СДО: 0, Всего: 0/0")

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.details_label)
        self.layout.addStretch()

    def update_summary(self, used_hours, planned_hours, details):
        """Обновляет отображаемую информацию"""
        used_total = used_hours['total']

        # Обновляем текст
        self.details_label.setText(
            f"Лекции: {used_hours['lecture']}, Практики: {used_hours['practice']}, "
            f"Сам.раб.: {used_hours['self_study']}, СДО: {used_hours['sdo']}, "
            f"Всего: {used_total}/{planned_hours}"
        )

        # Подсветка при превышении лимита
        if used_total > planned_hours:
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.details_label.setStyleSheet("color: red;")
        else:
            self.status_label.setStyleSheet("")
            self.details_label.setStyleSheet("")


class DisciplineForm(QWidget):
    def __init__(self):
        super().__init__()
        self.sdo_auto_calculated = True  # Флаг для отслеживания автоматического расчета СДО
        self.semester_hours = {}  # Словарь для хранения часов по семестрам
        self.semester_summary_widgets = {}  # Словарь для хранения виджетов сводки по семестрам
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Основная информация о дисциплине
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Название дисциплины:"))
        self.discipline_name = QLineEdit()
        info_layout.addWidget(self.discipline_name)

        layout.addLayout(info_layout)

        # Часы дисциплины
        hours_layout = QGridLayout()

        hours_layout.addWidget(QLabel("Общие часы:"), 0, 0)
        self.total_hours = QSpinBox()
        self.total_hours.setMaximum(1000)
        self.total_hours.valueChanged.connect(self.on_total_hours_changed)
        hours_layout.addWidget(self.total_hours, 0, 1)

        hours_layout.addWidget(QLabel("Лекции:"), 0, 2)
        self.lecture_hours = QSpinBox()
        self.lecture_hours.setMaximum(1000)
        self.lecture_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.lecture_hours, 0, 3)

        hours_layout.addWidget(QLabel("Практики:"), 1, 0)
        self.practice_hours = QSpinBox()
        self.practice_hours.setMaximum(1000)
        self.practice_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.practice_hours, 1, 1)

        hours_layout.addWidget(QLabel("Сам.раб.:"), 1, 2)
        self.self_study_hours = QSpinBox()
        self.self_study_hours.setMaximum(1000)
        self.self_study_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.self_study_hours, 1, 3)

        # Часы СДО
        hours_layout.addWidget(QLabel("СДО часы:"), 2, 0)
        self.sdo_hours = QSpinBox()
        self.sdo_hours.setMaximum(1000)
        self.sdo_hours.valueChanged.connect(self.on_sdo_hours_changed)
        hours_layout.addWidget(self.sdo_hours, 2, 1)

        # Чекбокс для автоматического расчета СДО
        self.sdo_auto_checkbox = QCheckBox("Автоматически (25% от общих часов)")
        self.sdo_auto_checkbox.setChecked(True)
        self.sdo_auto_checkbox.stateChanged.connect(self.on_sdo_auto_changed)
        hours_layout.addWidget(self.sdo_auto_checkbox, 2, 2, 1, 2)

        layout.addLayout(hours_layout)

        # Распределение часов по семестрам
        semester_group = QGroupBox("Распределение часов по семестрам")
        semester_layout = QVBoxLayout()

        # Контейнер для ввода часов по семестрам
        self.semester_container = QVBoxLayout()
        semester_layout.addLayout(self.semester_container)

        # Кнопка добавления семестра
        self.add_semester_btn = QPushButton("+ Добавить семестр")
        self.add_semester_btn.clicked.connect(self.add_semester)
        semester_layout.addWidget(self.add_semester_btn)

        semester_group.setLayout(semester_layout)
        layout.addWidget(semester_group)

        # Сводка по использованию часов в семестрах
        self.semester_summary_group = QGroupBox("Использование часов по семестрам")
        self.semester_summary_layout = QVBoxLayout()
        self.semester_summary_group.setLayout(self.semester_summary_layout)
        layout.addWidget(self.semester_summary_group)

        # Кнопка добавления раздела
        self.add_section_btn = QPushButton("+ Добавить раздел")
        self.add_section_btn.clicked.connect(self.add_section)
        layout.addWidget(self.add_section_btn)

        # Контейнер для разделов
        self.sections_container = QVBoxLayout()
        layout.addLayout(self.sections_container)

        # Статус проверки
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        # Кнопка сохранения
        self.save_btn = QPushButton("Сохранить программу")
        self.save_btn.clicked.connect(self.save_program)
        layout.addWidget(self.save_btn)

        self.sections = []
        self.add_section()  # Добавляем первый раздел по умолчанию
        self.add_semester()  # Добавляем первый семестр по умолчанию

    def add_semester(self):
        """Добавление нового семестра"""
        semester_layout = QHBoxLayout()

        semester_number = len(self.semester_hours) + 1

        semester_label = QLabel(f"Семестр {semester_number}:")
        hours_spin = QSpinBox()
        hours_spin.setMaximum(1000)
        hours_spin.valueChanged.connect(self.check_hours)

        # Сохраняем спинбокс в словарь
        self.semester_hours[semester_number] = hours_spin

        # Создаем виджет сводки для этого семестра
        summary_widget = SemesterSummaryWidget(semester_number)
        self.semester_summary_widgets[semester_number] = summary_widget
        self.semester_summary_layout.addWidget(summary_widget)

        semester_layout.addWidget(semester_label)
        semester_layout.addWidget(hours_spin)
        semester_layout.addStretch()

        self.semester_container.addLayout(semester_layout)

    def update_semester_summary(self):
        """Обновление сводки по использованию часов в семестрах"""
        # Считаем использованные часы по семестрам
        semester_usage = {}
        for semester in self.semester_hours:
            semester_usage[semester] = {
                'lecture': 0,
                'practice': 0,
                'self_study': 0,
                'sdo': 0,
                'total': 0
            }

        for section in self.sections:
            semester = section.get_semester()
            if semester in semester_usage:
                lecture, practice, self_study, sdo = section.get_hours_by_type()
                semester_usage[semester]['lecture'] += lecture
                semester_usage[semester]['practice'] += practice
                semester_usage[semester]['self_study'] += self_study
                semester_usage[semester]['sdo'] += sdo
                semester_usage[semester]['total'] += lecture + practice + self_study

        # Обновляем виджеты сводки
        for semester, summary_widget in self.semester_summary_widgets.items():
            if semester in self.semester_hours:
                used = semester_usage[semester]
                planned = self.semester_hours[semester].value()
                summary_widget.update_summary(used, planned, {})

    def on_total_hours_changed(self):
        """Обработчик изменения общих часов"""
        if self.sdo_auto_checkbox.isChecked():
            # Автоматически рассчитываем СДО как 25% от общих часов
            sdo_value = int(self.total_hours.value() * 0.25)
            self.sdo_hours.setValue(sdo_value)
            self.sdo_auto_calculated = True

        # Обновляем все разделы для проверки превышения часов
        for section in self.sections:
            section.on_hours_changed()

        self.check_hours()

    def on_sdo_hours_changed(self):
        """Обработчик изменения часов СДО"""
        self.sdo_auto_calculated = False
        self.sdo_auto_checkbox.setChecked(False)
        self.check_hours()

    def on_sdo_auto_changed(self, state):
        """Обработчик изменения состояния чекбокса автоматического расчета СДО"""
        if state == Qt.CheckState.Checked.value:
            # Включаем автоматический расчет
            sdo_value = int(self.total_hours.value() * 0.25)
            self.sdo_hours.setValue(sdo_value)
            self.sdo_auto_calculated = True
        else:
            self.sdo_auto_calculated = False

    def add_section(self):
        section = SectionWidget(self)
        section.hoursChanged.connect(self.check_hours)
        self.sections.append(section)
        self.sections_container.addWidget(section)

    def remove_section(self, section):
        self.sections.remove(section)
        section.deleteLater()
        self.check_hours()

    def check_hours(self):
        """Проверка соответствия часов"""
        total_lecture = 0
        total_practice = 0
        total_self_study = 0
        total_sdo = 0

        # Суммируем часы по всем разделам и темам
        for section in self.sections:
            lecture, practice, self_study, sdo = section.get_hours_by_type()
            total_lecture += lecture
            total_practice += practice
            total_self_study += self_study
            total_sdo += sdo

        total_calculated = total_lecture + total_practice + total_self_study

        # Обновляем сводку по семестрам
        self.update_semester_summary()

        # Проверяем соответствие
        is_lecture_match = total_lecture == self.lecture_hours.value()
        is_practice_match = total_practice == self.practice_hours.value()
        is_self_study_match = total_self_study == self.self_study_hours.value()
        is_total_match = total_calculated == self.total_hours.value()
        is_sdo_match = total_sdo == self.sdo_hours.value()

        # Проверяем превышение лимитов по семестрам
        semester_errors = []
        for semester, hours_spin in self.semester_hours.items():
            used_hours = 0
            for section in self.sections:
                if section.get_semester() == semester:
                    lecture, practice, self_study, sdo = section.get_hours_by_type()
                    used_hours += lecture + practice + self_study

            if used_hours > hours_spin.value():
                semester_errors.append(f"семестр {semester}")

        # Подсвечиваем несоответствия
        self.highlight_mismatch(self.lecture_hours, is_lecture_match)
        self.highlight_mismatch(self.practice_hours, is_practice_match)
        self.highlight_mismatch(self.self_study_hours, is_self_study_match)
        self.highlight_mismatch(self.total_hours, is_total_match)
        self.highlight_mismatch(self.sdo_hours, is_sdo_match)

        # Обновляем статус
        all_ok = all([is_lecture_match, is_practice_match, is_self_study_match, is_total_match,
                      is_sdo_match]) and not semester_errors
        if all_ok:
            self.status_label.setText("✓ Часы сбалансированы")
            self.status_label.setStyleSheet("color: green;")
        else:
            mismatches = []
            if not is_lecture_match:
                mismatches.append(f"лекции ({total_lecture} вместо {self.lecture_hours.value()})")
            if not is_practice_match:
                mismatches.append(f"практики ({total_practice} вместо {self.practice_hours.value()})")
            if not is_self_study_match:
                mismatches.append(f"самостоятельная работа ({total_self_study} вместо {self.self_study_hours.value()})")
            if not is_total_match:
                mismatches.append(f"общие часы ({total_calculated} вместо {self.total_hours.value()})")
            if not is_sdo_match:
                mismatches.append(f"СДО ({total_sdo} вместо {self.sdo_hours.value()})")

            if semester_errors:
                mismatches.append(f"превышение лимита в {', '.join(semester_errors)}")

            self.status_label.setText("✗ Несоответствие: " + ", ".join(mismatches))
            self.status_label.setStyleSheet("color: red;")

    def highlight_mismatch(self, widget, is_match):
        """Подсветка виджета при несоответствии"""
        if is_match:
            widget.setStyleSheet("")
        else:
            widget.setStyleSheet("background-color: #ffcccc;")

    def save_program(self):
        """Сохранение рабочей программы"""
        self.check_hours()

        # Проверяем, что все часы сбалансированы
        if "Несоответствие" not in self.status_label.text():
            # Собираем данные для сохранения
            program_data = {
                "discipline_name": self.discipline_name.text(),
                "total_hours": self.total_hours.value(),
                "lecture_hours": self.lecture_hours.value(),
                "practice_hours": self.practice_hours.value(),
                "self_study_hours": self.self_study_hours.value(),
                "sdo_hours": self.sdo_hours.value(),
                "sdo_auto_calculated": self.sdo_auto_calculated,
                "semester_hours": {semester: widget.value()
                                   for semester, widget in self.semester_hours.items()},
                "sections": []
            }

            for section in self.sections:
                section_data = {
                    "name": section.name_edit.text(),
                    "semester": section.semester_spin.value(),
                    "hours_summary": {
                        "lecture": section.section_lecture_label.text().split(": ")[1],
                        "practice": section.section_practice_label.text().split(": ")[1],
                        "self_study": section.section_self_study_label.text().split(": ")[1],
                        "sdo": section.section_sdo_label.text().split(": ")[1],
                        "total": section.section_total_label.text().split(": ")[1]
                    },
                    "topics": []
                }

                for topic in section.topics:
                    topic_data = {
                        "name": topic.name_edit.text(),
                        "hours_summary": {
                            "lecture": topic.lecture_label.text().split(": ")[1],
                            "practice": topic.practice_label.text().split(": ")[1],
                            "self_study": topic.self_study_label.text().split(": ")[1],
                            "sdo": topic.sdo_label.text().split(": ")[1],
                            "total": topic.total_label.text().split(": ")[1]
                        },
                        "activities": []
                    }

                    for activity in topic.activities:
                        activity_data = {
                            "name": activity.name_edit.text(),
                            "type": activity.type_combo.currentText(),
                            "hours": activity.hours_spin.value(),
                            "presence": activity.presence_combo.currentText()
                        }
                        topic_data["activities"].append(activity_data)

                    section_data["topics"].append(topic_data)

                program_data["sections"].append(section_data)

            # Здесь можно добавить логику сохранения данных в файл или БД
            print("Данные для сохранения:", program_data)

            QMessageBox.information(self, "Успех", "Рабочая программа сохранена!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не все часы сбалансированы!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Формирование рабочих программ")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QScrollArea()
        self.form = DisciplineForm()
        self.central_widget.setWidget(self.form)
        self.central_widget.setWidgetResizable(True)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())