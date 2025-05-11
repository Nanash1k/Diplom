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
            background: #ffffff;
            color: #333333;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый клиент")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+7 (999) 999-99-99;_")
        self.email_input = QLineEdit()

        input_style = """
            background: #ffffff;
            color: #333333;
            border: 1px solid #BBDEFB;
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