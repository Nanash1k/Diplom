from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QColor
from database import Client, Tour


class OrderForm(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Новый заказ")
        self.setFixedSize(600, 300)
        self.setStyleSheet("""
            background: #404040;
            color: #ddd;
            border-radius: 10px;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Оформление заказа")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 600;
            color: #9c27b0;
            padding-bottom: 10px;
        """)

        form = QFormLayout()
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        self.client_combo = QComboBox()
        self.tour_combo = QComboBox()
        self.status_combo = QComboBox()
        self.status_combo.addItems(["В работе", "Подтвержден", "Отменен"])

        combo_style = """
            QComboBox {
                background: #555;
                color: #ddd;
                border: 2px solid #666;
                border-radius: 5px;
                padding: 10px;
                min-height: 40px;
            }
            QComboBox:hover {
                border-color: #777;
            }
            QComboBox:focus {
                border-color: #9c27b0;
            }
            QComboBox QAbstractItemView {
                background: #555;
                color: #ddd;
                selection-background-color: #9c27b0;
            }
        """
        self.client_combo.setStyleSheet(combo_style)
        self.tour_combo.setStyleSheet(combo_style)
        self.status_combo.setStyleSheet(combo_style)

        for client in self.session.query(Client).all():
            self.client_combo.addItem(client.name, client.id)
        for tour in self.session.query(Tour).all():
            self.tour_combo.addItem(f"{tour.destination}", tour.id)

        form.addRow("Клиент:", self.client_combo)
        form.addRow("Тур:", self.tour_combo)
        form.addRow("Статус:", self.status_combo)

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