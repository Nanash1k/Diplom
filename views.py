from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTableView, QLabel, QPushButton, QHBoxLayout,
    QHeaderView, QAbstractItemView, QToolBar, QAction
)
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QPainter, QStandardItemModel, QStandardItem, QColor, QFont
from database import Client, Tour, Order
from widgets.client_form import ClientForm
from widgets.tour_form import TourForm
from widgets.order_form import OrderForm


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(150, 50)
        self.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: #ecf0f1;
                border-radius: 8px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("ТурМенеджер")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet("""
            QMainWindow { 
                background: #2c3e50; 
            }
            QTableView { 
                background: #34495e; 
                color: #ecf0f1;
                gridline-color: #2c3e50;
                font-size: 14px;
            }
            QHeaderView::section { 
                background: #3498db; 
                color: #ecf0f1; 
                padding: 15px;
                font-size: 14px;
            }
            QTabWidget::pane { 
                border: 0; 
            }
            QTabBar::tab {
                background: #34495e;
                color: #bdc3c7;
                padding: 10px 25px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected { 
                background: #3498db; 
                color: #ecf0f1;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Панель инструментов
        toolbar = QToolBar()
        buttons = [
            ("➕ Клиент", self.open_client_form),
            ("✈️ Тур", self.open_tour_form),
            ("📦 Заказ", self.open_order_form),
            ("🔄 Обновить", self.load_data)
        ]
        for text, callback in buttons:
            btn = AnimatedButton(text)
            btn.clicked.connect(callback)
            toolbar.addWidget(btn)
        layout.addWidget(toolbar)

        # Вкладки
        self.tabs = QTabWidget()
        self.setup_tabs()
        layout.addWidget(self.tabs)

    def setup_tabs(self):
        # Клиенты
        self.client_table = self.create_table(["Имя", "Телефон", "Email"])
        # Туры
        self.tour_table = self.create_table(["Направление", "Дата", "Цена", "Оператор"])
        # Заказы
        self.order_table = self.create_table(["Клиент", "Тур", "Статус"])
        # Статистика
        self.stats_tab = self.create_stats_tab()

        self.tabs.addTab(self.client_table, "Клиенты")
        self.tabs.addTab(self.tour_table, "Туры")
        self.tabs.addTab(self.order_table, "Заказы")
        self.tabs.addTab(self.stats_tab, "📊 Статистика")

    def create_table(self, headers):
        table = QTableView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        # Включаем номера строк
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setStyleSheet("""
            QHeaderView::section { 
                background: #3498db; 
                color: #ecf0f1;
            }
        """)

        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        return table

    def create_stats_tab(self):
        tab = QWidget()
        series = QPieSeries()
        tours = self.session.query(Tour).all()

        for tour in tours:
            count = self.session.query(Order).filter_by(tour_id=tour.id).count()
            series.append(f"{tour.destination} ({count})", count)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Распределение заказов")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QColor("#2c3e50"))
        chart.setTitleBrush(QColor("#ecf0f1"))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        tab.setLayout(layout)
        return tab

    def load_data(self):
        # Клиенты
        model = self.client_table.model()
        model.setRowCount(0)
        for client in self.session.query(Client).all():
            model.appendRow([
                QStandardItem(client.name),
                QStandardItem(client.phone),
                QStandardItem(client.email or "")
            ])

        # Туры
        model = self.tour_table.model()
        model.setRowCount(0)
        for tour in self.session.query(Tour).all():
            model.appendRow([
                QStandardItem(tour.destination),
                QStandardItem(tour.start_date.strftime("%d.%m.%Y")),
                QStandardItem(f"{tour.price} ₽"),
                QStandardItem(tour.operator or "")
            ])

        # Заказы
        model = self.order_table.model()
        model.setRowCount(0)
        for order in self.session.query(Order).join(Client).join(Tour).all():
            model.appendRow([
                QStandardItem(order.client.name),
                QStandardItem(order.tour.destination),
                QStandardItem(order.status)
            ])

    def open_client_form(self):
        form = ClientForm(self)
        if form.exec_():
            self.session.add(Client(
                name=form.name_input.text(),
                phone=form.phone_input.text(),
                email=form.email_input.text()
            ))
            self.session.commit()
            self.load_data()

    def open_tour_form(self):
        form = TourForm(self)
        if form.exec_():
            self.session.add(Tour(
                destination=form.destination_input.text(),
                start_date=form.date_input.date().toPyDate(),
                duration=form.duration_input.value(),
                price=form.price_input.value()
            ))
            self.session.commit()
            self.load_data()

    def open_order_form(self):
        form = OrderForm(self.session, self)
        if form.exec_():
            self.load_data()