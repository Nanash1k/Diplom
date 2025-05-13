from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit,
    QSpinBox, QDialogButtonBox, QVBoxLayout, QLabel, QSizePolicy
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor

class TourForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый тур")
        self.setMinimumSize(600, 500)
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

        title = QLabel("Создание тура")
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
            QLineEdit, QSpinBox, QDateEdit {
                background: #555;
                color: #ddd;
                border: 2px solid #666;
                border-radius: 5px;
                padding: 10px;
                min-height: 40px;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus, QDateEdit:focus {
                border-color: #9c27b0;
                background: #666;
            }
        """

        self.destination_input = QLineEdit()
        self.operator_input = QLineEdit()
        self.date_input = QDateEdit(QDate.currentDate().addDays(30))
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 30)
        self.price_input = QSpinBox()
        self.price_input.setRange(10000, 1000000)
        self.price_input.setPrefix("₽ ")
        self.adults_input = QSpinBox()
        self.adults_input.setRange(1, 100)
        self.adults_input.setValue(2)
        self.children_input = QSpinBox()
        self.children_input.setRange(0, 100)

        for widget in [self.destination_input, self.operator_input, self.date_input,
                       self.duration_input, self.price_input, self.adults_input,
                       self.children_input]:
            widget.setStyleSheet(input_style)

        form.addRow("Направление*:", self.destination_input)
        form.addRow("Оператор:", self.operator_input)
        form.addRow("Дата начала*:", self.date_input)
        form.addRow("Длительность (дни)*:", self.duration_input)
        form.addRow("Цена*:", self.price_input)
        form.addRow("Взрослые*:", self.adults_input)
        form.addRow("Дети:", self.children_input)

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