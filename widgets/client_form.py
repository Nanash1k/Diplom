from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont

class ClientForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый клиент")
        self.setFixedSize(500, 300)
        self.setStyleSheet("""
            background: #404040;
            color: #ffffff;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый клиент")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498db;")

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+7 (999) 999-99-99;_")
        self.email_input = QLineEdit()

        # Стили для полей ввода
        input_style = """
            background: #505050;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 5px;
        """
        self.name_input.setStyleSheet(input_style)
        self.phone_input.setStyleSheet(input_style)
        self.email_input.setStyleSheet(input_style)

        form.addRow("ФИО:", self.name_input)
        form.addRow("Телефон:", self.phone_input)
        form.addRow("Email:", self.email_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background: #505050;
                color: #ffffff;
                min-width: 80px;
                padding: 5px;
            }
            QPushButton:hover {
                background: #606060;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)