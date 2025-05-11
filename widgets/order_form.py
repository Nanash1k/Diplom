from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QComboBox,
    QDialogButtonBox, QVBoxLayout, QLabel
)
from database import Client, Tour


class OrderForm(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Новый заказ")
        self.setFixedSize(500, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Новый заказ")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")

        form = QFormLayout()
        self.client_combo = QComboBox()
        self.tour_combo = QComboBox()
        self.status_combo = QComboBox()
        self.status_combo.addItems(["В работе", "Подтвержден", "Отменен"])

        for client in self.session.query(Client).all():
            self.client_combo.addItem(client.name, client.id)
        for tour in self.session.query(Tour).all():
            self.tour_combo.addItem(f"{tour.destination} ({tour.start_date})", tour.id)

        form.addRow("Клиент:", self.client_combo)
        form.addRow("Тур:", self.tour_combo)
        form.addRow("Статус:", self.status_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)