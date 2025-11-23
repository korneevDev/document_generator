import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

from data import repository
from ui.widget.discipline_form import DisciplineForm


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список дисциплин")
        self.resize(900, 500)

        self.subjects = []  # список Subject

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # ---------------------------------------------------
        # Таблица
        # ---------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Код", "Название", "Обязательная", "Тип"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # --- таблица растягивается на всю ширину
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table, stretch=1)

        # ---------------------------------------------------
        # Кнопки
        # ---------------------------------------------------
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()  # отодвигает кнопки вправо

        self.add_btn = QPushButton("Добавить дисциплину")
        self.edit_btn = QPushButton("Редактировать")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)

        layout.addLayout(btn_layout)

        # ---------------------------------------------------
        # Сигналы
        # ---------------------------------------------------
        self.add_btn.clicked.connect(self.add_subject)
        self.edit_btn.clicked.connect(self.edit_subject)

        # ---------------------------------------------------
        # Загрузка данных
        # ---------------------------------------------------
        self.load_data()
        self.refresh_table()

    def load_data(self):
        self.subjects = repository.load_subjects()

    def refresh_table(self):
        self.table.setRowCount(len(self.subjects))
        for row, sub in enumerate(self.subjects):
            self.table.setItem(row, 0, QTableWidgetItem(sub.code))
            self.table.setItem(row, 1, QTableWidgetItem(sub.name))
            self.table.setItem(row, 2, QTableWidgetItem("Да" if sub.is_required else "Нет"))
            self.table.setItem(row, 3, QTableWidgetItem(sub.type))

    def add_subject(self):
        form = DisciplineForm()
        form.show()

    def edit_subject(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите строку")
            return

        subject = self.subjects[row]

        form = DisciplineForm(subject)
        form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
