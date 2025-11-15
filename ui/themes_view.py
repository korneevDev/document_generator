import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, pyqtSignal


class ActivityWidget(QWidget):
    activityChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название занятия")
        self.name_edit.textChanged.connect(self.on_activity_changed)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Лекция", "Практика", "Самостоятельная работа"])
        self.type_combo.currentTextChanged.connect(self.on_activity_changed)

        self.hours_spin = QSpinBox()
        self.hours_spin.setMaximum(1000)
        self.hours_spin.valueChanged.connect(self.on_activity_changed)

        self.presence_combo = QComboBox()
        self.presence_combo.addItems(["Очно", "СДО"])
        self.presence_combo.currentTextChanged.connect(self.on_activity_changed)

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
        self.activityChanged.emit()

    def delete_self(self):
        if self.parent():
            self.parent().remove_activity(self)


class TopicWidget(QWidget):
    hoursChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.activities = []

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

        self.activities_container = QVBoxLayout()
        self.layout.addLayout(self.activities_container)

        self.add_activity()

    def add_activity(self):
        activity = ActivityWidget(self)
        activity.activityChanged.connect(self.on_hours_changed)
        self.activities.append(activity)
        self.activities_container.addWidget(activity)
        self.on_hours_changed()

    def remove_activity(self, activity):
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
        if self.parent():
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


class SectionWidget(QWidget):
    hoursChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.topics = []

        # Header: name + semester selection
        self.header_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название раздела")
        self.name_edit.textChanged.connect(self.on_hours_changed)

        self.semester_combo = QComboBox()
        self._populate_semesters()
        self.semester_combo.currentIndexChanged.connect(self.on_hours_changed)

        self.add_topic_btn = QPushButton("+ Добавить тему")
        self.add_topic_btn.clicked.connect(self.add_topic)
        self.delete_btn = QPushButton("Удалить раздел")
        self.delete_btn.clicked.connect(self.delete_self)

        self.header_layout.addWidget(QLabel("Раздел:"))
        self.header_layout.addWidget(self.name_edit)
        self.header_layout.addWidget(QLabel("Семестр:"))
        self.header_layout.addWidget(self.semester_combo)
        self.header_layout.addWidget(self.add_topic_btn)
        self.header_layout.addWidget(self.delete_btn)
        self.header_layout.addStretch()

        self.layout.addLayout(self.header_layout)

        # Summary
        self.section_summary_layout = QHBoxLayout()
        self.section_lecture_label = QLabel("Лекции: 0")
        self.section_practice_label = QLabel("Практики: 0")
        self.section_self_study_label = QLabel("Сам.раб.: 0")
        self.section_sdo_label = QLabel("СДО: 0")
        self.section_total_label = QLabel("Всего: 0")

        self.section_summary_layout.addWidget(QLabel("Раздел:"))
        self.section_summary_layout.addWidget(self.section_lecture_label)
        self.section_summary_layout.addWidget(self.section_practice_label)
        self.section_summary_layout.addWidget(self.section_self_study_label)
        self.section_summary_layout.addWidget(self.section_sdo_label)
        self.section_summary_layout.addWidget(self.section_total_label)
        self.section_summary_layout.addStretch()

        self.layout.addLayout(self.section_summary_layout)

        # Topics container
        self.topics_container = QVBoxLayout()
        self.layout.addLayout(self.topics_container)

        self.add_topic()

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
        index = self.semester_combo.findData(current)
        if index != -1:
            self.semester_combo.setCurrentIndex(index)

    def add_topic(self):
        topic = TopicWidget(self)
        topic.hoursChanged.connect(self.on_hours_changed)
        self.topics.append(topic)
        self.topics_container.addWidget(topic)
        self.on_hours_changed()

    def remove_topic(self, topic):
        if topic in self.topics:
            self.topics.remove(topic)
            topic.deleteLater()
            self.on_hours_changed()

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

    def delete_self(self):
        if self.parent():
            self.parent().remove_section(self)

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


class SemesterSummaryWidget(QWidget):
    def __init__(self, semester_number, parent=None):
        super().__init__(parent)
        self.semester_number = semester_number
        self.layout = QHBoxLayout(self)

        self.status_label = QLabel(f"Семестр {semester_number}:")
        self.details_label = QLabel("Лекции: 0, Практики: 0, Сам.раб.: 0, СДО: 0, Всего: 0/0")

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.details_label)
        self.layout.addStretch()

    def update_summary(self, used_hours, planned_hours):
        used_total = used_hours['lecture'] + used_hours['practice'] + used_hours['self_study']
        planned_total = planned_hours.get('total', 0)

        self.details_label.setText(
            f"Лекции: {used_hours['lecture']}, Практики: {used_hours['practice']}, "
            f"Сам.раб.: {used_hours['self_study']}, СДО: {used_hours['sdo']}, "
            f"Всего: {used_total}/{planned_total}"
        )

        if used_total > planned_total:
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.details_label.setStyleSheet("color: red;")
        else:
            self.status_label.setStyleSheet("")
            self.details_label.setStyleSheet("")


class DisciplineForm(QWidget):
    def __init__(self):
        super().__init__()
        self.sdo_auto_calculated = True
        self.semester_hours = {}
        self.semester_summary_widgets = {}
        self._semester_numbers = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Название дисциплины:"))
        self.discipline_name = QLineEdit()
        info_layout.addWidget(self.discipline_name)
        layout.addLayout(info_layout)

        # Discipline totals
        hours_layout = QGridLayout()

        hours_layout.addWidget(QLabel("Общие часы:"), 0, 0)
        self.total_hours = QSpinBox(); self.total_hours.setMaximum(10000)
        self.total_hours.valueChanged.connect(self.on_total_hours_changed)
        hours_layout.addWidget(self.total_hours, 0, 1)

        hours_layout.addWidget(QLabel("Лекции:"), 0, 2)
        self.lecture_hours = QSpinBox(); self.lecture_hours.setMaximum(10000)
        self.lecture_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.lecture_hours, 0, 3)

        hours_layout.addWidget(QLabel("Практики:"), 1, 0)
        self.practice_hours = QSpinBox(); self.practice_hours.setMaximum(10000)
        self.practice_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.practice_hours, 1, 1)

        hours_layout.addWidget(QLabel("Сам.раб.:"), 1, 2)
        self.self_study_hours = QSpinBox(); self.self_study_hours.setMaximum(10000)
        self.self_study_hours.valueChanged.connect(self.check_hours)
        hours_layout.addWidget(self.self_study_hours, 1, 3)

        # SDO
        hours_layout.addWidget(QLabel("СДО часы:"), 2, 0)
        self.sdo_hours = QSpinBox(); self.sdo_hours.setMaximum(10000)
        self.sdo_hours.valueChanged.connect(self.on_sdo_hours_changed)
        hours_layout.addWidget(self.sdo_hours, 2, 1)

        self.sdo_auto_checkbox = QCheckBox("Автоматически (25% от общих часов)")
        self.sdo_auto_checkbox.setChecked(True)
        self.sdo_auto_checkbox.stateChanged.connect(self.on_sdo_auto_changed)
        hours_layout.addWidget(self.sdo_auto_checkbox, 2, 2, 1, 2)

        layout.addLayout(hours_layout)

        # Semester management
        sem_manage_group = QGroupBox("Настройка семестров")
        sem_manage_layout = QHBoxLayout()
        sem_manage_layout.addWidget(QLabel("Первый семестр:"))
        self.first_semester_spin = QSpinBox(); self.first_semester_spin.setRange(1, 20); self.first_semester_spin.setValue(1)
        sem_manage_layout.addWidget(self.first_semester_spin)
        sem_manage_layout.addWidget(QLabel("Количество семестров:"))
        self.semesters_count_spin = QSpinBox(); self.semesters_count_spin.setRange(1, 12); self.semesters_count_spin.setValue(1)
        sem_manage_layout.addWidget(self.semesters_count_spin)
        self.apply_semesters_btn = QPushButton("Применить семестры")
        self.apply_semesters_btn.clicked.connect(self.build_semesters)
        sem_manage_layout.addWidget(self.apply_semesters_btn)
        sem_manage_layout.addStretch()
        sem_manage_group.setLayout(sem_manage_layout)
        layout.addWidget(sem_manage_group)

        # Semester plan inputs (per-type + total)
        semester_group = QGroupBox("План часов по семестрам (введите по типам)")
        semester_layout = QVBoxLayout()
        self.semester_container = QVBoxLayout()
        semester_layout.addLayout(self.semester_container)
        semester_group.setLayout(semester_layout)
        layout.addWidget(semester_group)

        # Summary widgets
        self.semester_summary_group = QGroupBox("Использование часов по семестрам")
        self.semester_summary_layout = QVBoxLayout()
        self.semester_summary_group.setLayout(self.semester_summary_layout)
        layout.addWidget(self.semester_summary_group)

        # Sections
        self.add_section_btn = QPushButton("+ Добавить раздел")
        self.add_section_btn.clicked.connect(self.add_section)
        layout.addWidget(self.add_section_btn)

        self.sections_container = QVBoxLayout()
        layout.addLayout(self.sections_container)

        # Status & Save
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.save_btn = QPushButton("Сохранить программу")
        self.save_btn.clicked.connect(self.save_program)
        layout.addWidget(self.save_btn)

        self.sections = []

        # initialize semesters and one section
        self.build_semesters()
        self.add_section()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                child = item.layout()
                if child:
                    self.clear_layout(child)

    # ====================== Build semesters =========================
    def build_semesters(self):
        first = self.first_semester_spin.value()
        count = self.semesters_count_spin.value()
        new_nums = [first + i for i in range(count)]

        # save old values
        old_values = {}
        for num, d in self.semester_hours.items():
            old_values[num] = {
                'lecture': d['lecture'].value(),
                'practice': d['practice'].value(),
                'self_study': d['self_study'].value(),
                'sdo': d['sdo'].value(),
                'total': d['total'].value()
            }

        # clear old UI
        self.clear_layout(self.semester_container)
        self.clear_layout(self.semester_summary_layout)
        self.semester_hours.clear()
        self.semester_summary_widgets.clear()
        self._semester_numbers = new_nums

        for num in new_nums:
            row = QHBoxLayout()
            lbl = QLabel(f"Семестр {num}:")

            spin_lecture = QSpinBox(); spin_lecture.setMaximum(10000)
            spin_practice = QSpinBox(); spin_practice.setMaximum(10000)
            spin_self = QSpinBox(); spin_self.setMaximum(10000)
            spin_sdo = QSpinBox(); spin_sdo.setMaximum(10000)
            spin_total = QSpinBox(); spin_total.setMaximum(10000)

            # restore old values
            if num in old_values:
                spin_lecture.setValue(old_values[num]['lecture'])
                spin_practice.setValue(old_values[num]['practice'])
                spin_self.setValue(old_values[num]['self_study'])
                spin_sdo.setValue(old_values[num]['sdo'])
                spin_total.setValue(old_values[num]['total'])

            spin_lecture.valueChanged.connect(self.check_hours)
            spin_practice.valueChanged.connect(self.check_hours)
            spin_self.valueChanged.connect(self.check_hours)
            spin_sdo.valueChanged.connect(self.check_hours)
            spin_total.valueChanged.connect(self.check_hours)

            row.addWidget(lbl)
            row.addWidget(QLabel("Лекции:")); row.addWidget(spin_lecture)
            row.addWidget(QLabel("Практики:")); row.addWidget(spin_practice)
            row.addWidget(QLabel("Сам.раб.:")); row.addWidget(spin_self)
            row.addWidget(QLabel("СДО:")); row.addWidget(spin_sdo)
            row.addWidget(QLabel("Всего:")); row.addWidget(spin_total)
            row.addStretch()

            self.semester_container.addLayout(row)

            self.semester_hours[num] = {
                'lecture': spin_lecture,
                'practice': spin_practice,
                'self_study': spin_self,
                'sdo': spin_sdo,
                'total': spin_total
            }

            summary_widget = SemesterSummaryWidget(num)
            self.semester_summary_widgets[num] = summary_widget
            self.semester_summary_layout.addWidget(summary_widget)

        # update sections' semester combo boxes
        for section in self.sections:
            if hasattr(section, "update_semester_options"):
                section.update_semester_options()

        self.check_hours()

    def get_semester_numbers(self):
        return self._semester_numbers

    # ====================== Sections =========================
    def add_section(self):
        section = SectionWidget(self)
        section.hoursChanged.connect(self.check_hours)
        self.sections.append(section)
        self.sections_container.addWidget(section)
        self.check_hours()

    def remove_section(self, section):
        if section in self.sections:
            self.sections.remove(section)
            section.deleteLater()
            self.check_hours()

    # ====================== SDO =========================
    def on_sdo_auto_changed(self, state):
        self.sdo_auto_calculated = state == Qt.CheckState.Checked
        self.on_sdo_hours_changed()

    def on_total_hours_changed(self, value):
        if self.sdo_auto_calculated:
            auto_sdo = round(value * 0.25)
            self.sdo_hours.setValue(auto_sdo)
        self.check_hours()

    def on_sdo_hours_changed(self):
        self.check_hours()

    # ====================== Check Hours =========================
    def check_hours(self):
        semester_aggregates = {num: {'lecture':0, 'practice':0, 'self_study':0, 'sdo':0} for num in self._semester_numbers}

        # aggregate from sections
        for section in self.sections:
            sem = section.get_semester()
            lecture, practice, self_study, sdo = section.get_hours_by_type()
            if sem in semester_aggregates:
                semester_aggregates[sem]['lecture'] += lecture
                semester_aggregates[sem]['practice'] += practice
                semester_aggregates[sem]['self_study'] += self_study
                semester_aggregates[sem]['sdo'] += sdo

        # check against semester plan
        for num in self._semester_numbers:
            planned = self.semester_hours.get(num)
            if planned is None:
                continue
            planned_vals = {
                'lecture': planned['lecture'].value(),
                'practice': planned['practice'].value(),
                'self_study': planned['self_study'].value(),
                'sdo': planned['sdo'].value(),
                'total': planned['total'].value()
            }
            used = semester_aggregates[num]

            # update summary widget
            if num in self.semester_summary_widgets:
                self.semester_summary_widgets[num].update_summary(used, planned_vals)

            # highlight mismatches
            self._highlight_semester_plan(num, used, planned_vals)

    def _highlight_semester_plan(self, sem_num, used, planned):
        if sem_num not in self.semester_hours:
            return
        boxes = self.semester_hours[sem_num]
        boxes['lecture'].setStyleSheet("" if used['lecture'] == planned['lecture'] else "background-color: #ffdddd;")
        boxes['practice'].setStyleSheet("" if used['practice'] == planned['practice'] else "background-color: #ffdddd;")
        boxes['self_study'].setStyleSheet("" if used['self_study'] == planned['self_study'] else "background-color: #ffdddd;")
        boxes['sdo'].setStyleSheet("" if used['sdo'] == planned['sdo'] else "background-color: #ffdddd;")
        used_total = used['lecture'] + used['practice'] + used['self_study']
        boxes['total'].setStyleSheet("" if used_total == planned['total'] else "background-color: #ffdddd;")

    # ====================== Save =========================
    def save_program(self):
        msg = QMessageBox()
        msg.setWindowTitle("Сохранение")
        msg.setText("Программа успешно сохранена!")
        msg.exec()


# ====================== Main =========================
def main():
    app = QApplication(sys.argv)
    win = DisciplineForm()
    win.resize(1200, 800)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
