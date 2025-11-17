from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout, QMessageBox, QPushButton, QCheckBox, QVBoxLayout, \
    QLineEdit, QComboBox

from domain_types.practice_numerator import PracticeNumerator
from domain_types.subject import Subject
from ui.widget.section_widget import SectionWidget
from ui.widget.semester_summary_widget import SemesterSummaryWidget


class DisciplineForm(QWidget):
    discipline_name: QLineEdit
    discipline_code: QLineEdit
    first_semester_spin: QSpinBox
    semesters_count_spin: QSpinBox
    total_hours: QSpinBox
    lecture_hours: QSpinBox
    practice_hours: QSpinBox
    self_study_hours: QSpinBox
    sdo_hours: QSpinBox
    sdo_auto_checkbox: QCheckBox
    apply_semesters_btn: QPushButton
    add_section_btn: QPushButton
    save_btn: QPushButton

    discipline_is_require: QCheckBox
    exam_type_combo_box: QComboBox
    exam_cons_hours: QSpinBox
    exam_hours: QSpinBox
    course_hours: QSpinBox

    semester_container: QVBoxLayout
    semester_summary_layout: QVBoxLayout
    sections_container: QVBoxLayout
    status_label: QLabel
    practice_numerator : PracticeNumerator

    def __init__(self, base_ui_dir='./layout/'):
        super().__init__()

        uic.loadUi(base_ui_dir + 'discipline_form.ui', self)
        self.sdo_auto_calculated = True
        self.semester_hours = {}
        self.semester_summary_widgets = {}
        self._semester_numbers = []

        self.practice_numerator = PracticeNumerator()

        self.total_hours.valueChanged.connect(self.on_total_hours_changed)
        self.lecture_hours.valueChanged.connect(self.check_hours)
        self.practice_hours.valueChanged.connect(self.check_hours)
        self.self_study_hours.valueChanged.connect(self.check_hours)
        self.sdo_hours.valueChanged.connect(self.on_sdo_hours_changed)
        self.sdo_auto_checkbox.stateChanged.connect(self.on_sdo_auto_changed)

        self.apply_semesters_btn.clicked.connect(self.build_semesters)
        self.add_section_btn.clicked.connect(self.add_section)
        self.save_btn.clicked.connect(self.save_program)

        self.sections = []

        # initialize semesters and one section
        self.build_semesters()
        self.add_section()

        self.on_sdo_auto_changed(2)

    def fill_data(self, name):
        self.discipline_name.setText(name)
        self.discipline_name.setEnabled(False)

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

            spin_lecture = QSpinBox();
            spin_lecture.setMaximum(10000)
            spin_practice = QSpinBox();
            spin_practice.setMaximum(10000)
            spin_self = QSpinBox();
            spin_self.setMaximum(10000)
            spin_sdo = QSpinBox();
            spin_sdo.setMaximum(10000)
            spin_total = QSpinBox();
            spin_total.setMaximum(10000)

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
            row.addWidget(QLabel("Лекции:"));
            row.addWidget(spin_lecture)
            row.addWidget(QLabel("Практики:"));
            row.addWidget(spin_practice)
            row.addWidget(QLabel("Сам.раб.:"));
            row.addWidget(spin_self)
            row.addWidget(QLabel("СДО:"));
            row.addWidget(spin_sdo)
            row.addWidget(QLabel("Всего:"));
            row.addWidget(spin_total)
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
        section = SectionWidget(controller=self, numerator=self.practice_numerator)
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
        if state == 2:
            self.sdo_auto_calculated = True
            self.sdo_hours.setEnabled(False)
            self.on_total_hours_changed(self.total_hours.value())
            self.on_sdo_hours_changed()
        else:
            self.sdo_auto_calculated = False
            self.sdo_hours.setEnabled(True)

    def on_total_hours_changed(self, value):
        if self.sdo_auto_calculated:
            auto_sdo = round(value * 0.25)
            self.sdo_hours.setValue(auto_sdo)
        self.check_hours()

    def on_sdo_hours_changed(self):
        self.check_hours()

    # ====================== Check Hours =========================
    def check_hours(self):
        semester_aggregates = {num: {'lecture': 0, 'practice': 0, 'self_study': 0, 'sdo': 0} for num in
                               self._semester_numbers}

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

        # ======== GLOBAL HOURS CONSISTENCY CHECK ========
        self.check_global_hours(semester_aggregates)

    def _highlight_semester_plan(self, sem_num, used, planned):
        if sem_num not in self.semester_hours:
            return
        boxes = self.semester_hours[sem_num]
        boxes['lecture'].setStyleSheet("" if used['lecture'] == planned['lecture'] else "background-color: #ffdddd;")
        boxes['practice'].setStyleSheet("" if used['practice'] == planned['practice'] else "background-color: #ffdddd;")
        boxes['self_study'].setStyleSheet(
            "" if used['self_study'] == planned['self_study'] else "background-color: #ffdddd;")
        boxes['sdo'].setStyleSheet("" if used['sdo'] == planned['sdo'] else "background-color: #ffdddd;")
        used_total = used['lecture'] + used['practice'] + used['self_study']
        boxes['total'].setStyleSheet("" if used_total == planned['total'] else "background-color: #ffdddd;")

    # ====================== Global consistency check =========================
    def check_global_hours(self, semester_aggregates):
        """
        Проверяет:
        1. Общие часы дисциплины = План по семестрам = Фактические часы
        2. Подсвечивает ошибки и обновляет status_label
        """

        # 1. Общие часы дисциплины (заявленные)
        declared_total = self.total_hours.value()

        # 2. Фактические часы (разделы)
        fact_lecture = fact_practice = fact_self = 0
        for section in self.sections:
            lec, pract, self_s, _ = section.get_hours_by_type()
            fact_lecture += lec
            fact_practice += pract
            fact_self += self_s

        fact_total = fact_lecture + fact_practice + fact_self

        # 3. План по семестрам (сумма total полей)
        planned_lecture = planned_practice = planned_self = 0
        planned_total = 0

        for num in self._semester_numbers:
            plan_box = self.semester_hours.get(num)
            if plan_box:
                planned_lecture += plan_box['lecture'].value()
                planned_practice += plan_box['practice'].value()
                planned_self += plan_box['self_study'].value()
                planned_total += plan_box['total'].value()

        # сравнение суммарных значений
        errors = []

        if declared_total != planned_total:
            errors.append(f"Ошибка: общие часы дисциплины ({declared_total}) ≠ суммы по семестрам ({planned_total})")

        if declared_total != fact_total:
            errors.append(
                f"Ошибка: общие часы дисциплины ({declared_total}) ≠ фактически распределённым ({fact_total})")

        if fact_total != planned_total:
            errors.append(f"Ошибка: фактически распределено ({fact_total}) ≠ плану по семестрам ({planned_total})")

        # Подсветка total_hours spinbox
        if declared_total == fact_total == planned_total:
            self.total_hours.setStyleSheet("")
        else:
            self.total_hours.setStyleSheet("background-color: #ffdddd;")

        # ======= UI reaction =======
        if errors:
            self.status_label.setText("\n".join(errors))
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.status_label.setText("Часы согласованы")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")

    # ====================== Save =========================
    def save_program(self):
        # Prevent saving if inconsistent (optional behavior)
        # You can enable blocking save when inconsistencies exist by uncommenting the check below.
        """
        if "Ошибка" in self.status_label.text():
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Невозможно сохранить: обнаружены несогласованные часы.")
            msg.exec()
            return
        """
        msg = QMessageBox()
        msg.setWindowTitle("Сохранение")

        subject = Subject(self.discipline_code.text(), self.discipline_name.text(),
                          self.discipline_is_require.checkState() == Qt.CheckState.Checked,
                          self.exam_type_combo_box.currentText() == 'Экзамен', self.exam_hours.value(), self.exam_cons_hours.value(), None, None, None, None)

        print(subject)

        chapters = []

        for section in self.sections:
            chapters.append(section.get_data())

        print(chapters)

        msg.setText("Программа успешно сохранена!")
        msg.exec()
