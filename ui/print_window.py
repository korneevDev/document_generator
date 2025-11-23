# -------------------------------------------------------
# Главное окно формы
# -------------------------------------------------------
import sys
import datetime

from PyQt6.QtWidgets import (
    QMessageBox, QApplication, QComboBox, QPushButton,
    QWidget, QFormLayout, QSpinBox
)

from data import repository
from domain_types.organization import Organization, Worker, Department
from domain_types.skills import CommonProfSkills
from domain_types.subject import SubjectYear
from main import generate_document_with_deletion
from view_types.doc_task_view_model import DocumentTaskView
from view_types.program_view_model import ProgramViewModel
from view_types.view_skill_type import CommonProfSkillsView, ResultsView

# -------------------------------------------------------
# Заглушки — потом заменишь реальными репозиториями
# -------------------------------------------------------
def get_organizations() -> list[Organization]:
    return repository.load_organizations()


def get_workers() -> list[Worker]:
    return repository.load_workers()


def get_departments() -> list[Department]:
    return repository.load_departments()


def get_programs() -> list[ProgramViewModel]:
    return repository.load_programs()


# -------------------------------------------------------
# Окно создания DocumentTaskView
# -------------------------------------------------------
class DocumentTaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Создание DocumentTaskView")
        self.resize(400, 300)

        layout = QFormLayout()
        self.setLayout(layout)

        # --- Organization ---
        self.org_cb = self.create_combo(get_organizations())
        layout.addRow("Организация:", self.org_cb)

        # --- Workers ---
        # Пока один, т.к. мультивыбор ты потом сделаешь
        self.worker_cb = self.create_combo(get_workers())
        layout.addRow("Работник:", self.worker_cb)

        # --- Department ---
        self.department_cb = self.create_combo(get_departments())
        layout.addRow("Отдел:", self.department_cb)

        # --- Program (profile) ---
        self.profile_cb = self.create_combo(get_programs())
        layout.addRow("Профиль:", self.profile_cb)

        # Save button
        save_btn = QPushButton("Создать")
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)

    # -------------------------------------------------------
    # Комбобокс с поддержкой data
    # -------------------------------------------------------
    def create_combo(self, items):
        cb = QComboBox()
        cb.setEditable(True)

        for item in items:
            cb.addItem(str(item), item)

        return cb

    # -------------------------------------------------------
    # Сохранение — создаем DocumentTaskView
    # -------------------------------------------------------
    def save(self):
        doc = DocumentTaskView(
            delete_marker='{delete}',
            organization=self.org_cb.currentData(),
            workers=[self.worker_cb.currentData()],
            department=self.department_cb.currentData(),
            profile=self.profile_cb.currentData(),
            subject=self.subject,
            skills=self.skills.map_to_view(),
            results=self.results,
        )

        print(doc.subject.exam_questions.practice)

        generate_document_with_deletion(
            "../static/templates/cesi_template_op.docx",
            f"../output/{doc.subject.type}.{doc.subject.code}_{doc.subject.year}_{datetime.datetime.now().strftime('%H-%M-%S')}.docx",
            doc.__dict__
        )

        QMessageBox.information(self, "Готово", f"DocumentTaskView:\n{doc}")

    def set_subject(self, subject, skills, results):
        self.subject = subject
        self.skills : CommonProfSkills = skills
        self.results = results


# -------------------------------------------------------
# Запуск
# -------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DocumentTaskWindow()
    win.show()
    sys.exit(app.exec())
