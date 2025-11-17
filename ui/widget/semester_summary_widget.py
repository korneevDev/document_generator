from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel


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
