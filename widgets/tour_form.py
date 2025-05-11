from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit,
    QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtCore import QDate

class TourForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый тур")
        self.setFixedSize(500, 350)
        self.setStyleSheet("""
            background: #ffffff;
            color: #333333;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый тур")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db;")

        form = QFormLayout()
        self.destination_input = QLineEdit()
        self.date_input = QDateEdit(QDate.currentDate().addDays(30))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 30)
        self.price_input = QSpinBox()
        self.price_input.setRange(10000, 1000000)

        form.addRow("Направление:", self.destination_input)
        form.addRow("Дата начала:", self.date_input)
        form.addRow("Длительность (дни):", self.duration_input)
        form.addRow("Цена (₽):", self.price_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)