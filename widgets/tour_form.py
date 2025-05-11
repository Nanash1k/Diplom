from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit,
    QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtCore import QDate


class TourForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый тур")
        self.setFixedSize(500, 450)
        self.setStyleSheet("""
            background: #ffffff;
            color: #333333;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый тур")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")

        form = QFormLayout()

        # Основные поля
        self.destination_input = QLineEdit()
        self.operator_input = QLineEdit()
        self.date_input = QDateEdit(QDate.currentDate().addDays(30))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 30)
        self.price_input = QSpinBox()
        self.price_input.setRange(10000, 1000000)
        self.price_input.setPrefix("₽ ")

        # Новые поля
        self.adults_input = QSpinBox()
        self.adults_input.setRange(1, 100)
        self.adults_input.setValue(2)
        self.children_input = QSpinBox()
        self.children_input.setRange(0, 100)

        # Стилизация полей
        input_style = """
            background: #ffffff;
            color: #333333;
            border: 1px solid #BBDEFB;
            padding: 5px;
        """
        for widget in [self.destination_input, self.operator_input, self.date_input,
                       self.duration_input, self.price_input, self.adults_input, self.children_input]:
            widget.setStyleSheet(input_style)

        # Добавление в форму
        form.addRow("Направление*:", self.destination_input)
        form.addRow("Оператор:", self.operator_input)
        form.addRow("Дата начала*:", self.date_input)
        form.addRow("Длительность (дни)*:", self.duration_input)
        form.addRow("Цена*:", self.price_input)
        form.addRow("Взрослые*:", self.adults_input)
        form.addRow("Дети:", self.children_input)

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: #ffffff;
                min-width: 80px;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)