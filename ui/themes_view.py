import sys

from PyQt6.QtWidgets import *

from ui.widget.discipline_form import DisciplineForm

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

# ========================== Главное окно ==========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список дисциплин")
        self.setGeometry(100, 100, 700, 400)

        self.disciplines = []  # Список дисциплин (список словарей)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Таблица дисциплин
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Название", "Общие часы", "Семестр", "Направление"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Только просмотр
        layout.addWidget(self.table)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить дисциплину")
        self.edit_btn = QPushButton("Редактировать выделенную")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        layout.addLayout(btn_layout)

        # Подключаем кнопки
        self.add_btn.clicked.connect(self.add_discipline)
        self.edit_btn.clicked.connect(self.edit_discipline)

        # Для примера: добавим несколько дисциплин
        self.add_sample_data()
        self.refresh_table()

    def add_sample_data(self):
        self.disciplines.append({"name": "Математика", "hours": 120, "semester": 1, "direction": "Физика"})
        self.disciplines.append({"name": "Программирование", "hours": 180, "semester": 2, "direction": "ИТ"})

    def refresh_table(self):
        self.table.setRowCount(len(self.disciplines))
        for row, disc in enumerate(self.disciplines):
            self.table.setItem(row, 0, QTableWidgetItem(disc["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(disc["hours"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(disc["semester"])))
            self.table.setItem(row, 3, QTableWidgetItem(disc["direction"]))

    def add_discipline(self):
        form = DisciplineForm()
        form.show()
        form.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def edit_discipline(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Внимание", "Выберите дисциплину для редактирования")
            return
        disc = self.disciplines[selected]
        form = DisciplineForm()
        form.fill_data(disc['name'])
        form.show()
        form.setWindowTitle(f"Редактирование: {disc['name']}")
        form.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)


# ========================== Запуск ==========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
