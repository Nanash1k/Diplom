from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QVBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class ClientForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый клиент")
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("""
            QDialog {
                background: #404040;
                color: #ddd;
                border-radius: 10px;
            }
            QLayout {
                margin: 15px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Новый клиент")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 600;
            color: #9c27b0;
            padding-bottom: 10px;
        """)

        form = QFormLayout()
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        input_style = """
            QLineEdit {
                background: #555;
                color: #ddd;
                border: 2px solid #666;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #9c27b0;
                background: #666;
            }
        """

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.phone_input.setInputMask("+7 (999) 999-99-99;_")
        self.email_input = QLineEdit()
        self.passport_input = QLineEdit()
        self.passport_input.setInputMask("9999 999999;_")

        for input in [self.name_input, self.phone_input, self.email_input, self.passport_input]:
            input.setStyleSheet(input_style)
            input.setMinimumHeight(40)

        form.addRow("ФИО*:", self.name_input)
        form.addRow("Телефон*:", self.phone_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Паспорт*:", self.passport_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet("""
            QPushButton {
                background: #9c27b0;
                color: white;
                min-width: 100px;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #8e24aa;
            }
            QPushButton:pressed {
                background: #7b1fa2;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)