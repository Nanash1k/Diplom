from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from PyQt5.QtGui import QFont
from database import Client, Tour

class OrderForm(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Новый заказ")
        self.setFixedSize(500, 250)
        self.setStyleSheet("""
            background: #ffffff;
            color: #333333;
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый заказ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2196F3;")

        form = QFormLayout()
        self.client_combo = QComboBox()
        self.tour_combo = QComboBox()
        self.status_combo = QComboBox()
        self.status_combo.addItems(["В работе", "Подтвержден", "Отменен"])

        for client in self.session.query(Client).all():
            self.client_combo.addItem(client.name, client.id)  # Важно: client.id
        for tour in self.session.query(Tour).all():
            self.tour_combo.addItem(f"{tour.destination}", tour.id)  # tour.id

        combo_style = """
            QComboBox {
                background: #ffffff;
                color: #333333;
                border: 1px solid #BBDEFB;
                padding: 5px;
            }
        """
        self.client_combo.setStyleSheet(combo_style)
        self.tour_combo.setStyleSheet(combo_style)
        self.status_combo.setStyleSheet(combo_style)

        form.addRow("Клиент:", self.client_combo)
        form.addRow("Тур:", self.tour_combo)
        form.addRow("Статус:", self.status_combo)

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