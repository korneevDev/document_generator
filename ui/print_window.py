# -------------------------------------------------------
# Главное окно формы
# -------------------------------------------------------
import sys

from PyQt6.QtWidgets import QMessageBox, QApplication, QComboBox, QPushButton, QWidget, QFormLayout, QSpinBox

from domain_types.doc_task_model import DocumentTask
from domain_types.organization import Organization
from domain_types.skills import Results, ProfessionalSkills, CommonProfSkills, Skill
from domain_types.subject import Subject, Room, Books, ExamQuestions
from view_types.view_skill_type import ProfessionalSkillsView


def get_chapters():
    return []


def get_organizations():
    return []


def get_workers():
    return []

def get_departments():
    return []


def get_programs():
    return []


def get_subjects():
    return []


def get_skills():
    return []

def get_results():
    return []

def get_programs_by_organization(id):
    return []


class DocumentTaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создание DocumentTask")
        self.resize(400, 300)

        layout = QFormLayout()
        self.setLayout(layout)

        # --- Organization ---
        self.org_cb = self.create_combo(get_organizations())
        layout.addRow("Организация:", self.org_cb)
        self.org_cb.currentTextChanged.connect(self.on_org_changed)

        # --- Workers (несколько, но оставим простой ComboBox, потом можно мультивыбор) ---
        self.worker_cb = self.create_combo(get_workers())
        layout.addRow("Работник:", self.worker_cb)

        # --- Department ---
        self.department_cb = self.create_combo(get_departments())
        layout.addRow("Отдел:", self.department_cb)

        # --- Year ---
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(2025)
        layout.addRow("Год:", self.year_spin)

        # --- Profile / Program ---
        self.profile_cb = self.create_combo(get_programs())
        layout.addRow("Профиль:", self.profile_cb)

        # --- Subject ---
        self.subject_cb = self.create_combo(get_subjects())
        layout.addRow("Дисциплина:", self.subject_cb)

        # --- Skills ---
        self.skills_cb = self.create_combo(get_skills())
        layout.addRow("Навыки (ОПК):", self.skills_cb)

        # --- Results ---
        self.results_cb = self.create_combo(get_results())
        layout.addRow("Результаты:", self.results_cb)

        # --- Chapters ---
        self.chapters_cb = self.create_combo(get_chapters())
        layout.addRow("Раздел:", self.chapters_cb)

        # Save button
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)

    def on_org_changed(self):
        org = self.org_cb.currentData()

        if org is None:
            self.profile_cb.clear()
            return

        programs = get_programs_by_organization(1)

        self.profile_cb.clear()
        for p in programs:
            self.profile_cb.addItem(p)

    # -------------------------------------------------------
    # Комбобокс с возможностью ввода текста
    # -------------------------------------------------------
    def create_combo(self, items):
        cb = QComboBox()
        cb.setEditable(True)
        for item in items:
            cb.addItem(str(item), item)
        return cb

    # -------------------------------------------------------
    # Сохранение документа
    # -------------------------------------------------------
    def save(self):
        doc = DocumentTask(
            '{delete}',
            organization=self.org_cb.currentData(),
            workers=[self.worker_cb.currentData()],
            department=self.department_cb.currentData(),
            year=self.year_spin.value(),
            profile=self.profile_cb.currentData(),
            subject=self.subject_cb.currentData(),
            skills=self.skills_cb.currentData(),
            results=self.results_cb.currentData(),
            chapters=[self.chapters_cb.currentData()],
        )

        QMessageBox.information(self, "Сохранено",
                                f"DocumentTask создан:\n{doc}")


# -------------------------------------------------------
# Запуск
# -------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DocumentTaskWindow()
    win.show()
    sys.exit(app.exec())