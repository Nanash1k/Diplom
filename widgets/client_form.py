from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtCore import QPropertyAnimation


class ClientForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый клиент")
        self.setFixedSize(500, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый клиент")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+7 (999) 999-99-99;_")
        self.email_input = QLineEdit()

        form.addRow("ФИО:", self.name_input)
        form.addRow("Телефон:", self.phone_input)
        form.addRow("Email:", self.email_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)