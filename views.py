from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTableView, QLabel, QPushButton, QHBoxLayout,
    QHeaderView, QAbstractItemView, QToolBar, QAction, QMessageBox
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
                background: #404040;
                color: #ffffff;
                border-radius: 8px;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #555555;
            }
            QPushButton:hover {
                background: #505050;
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
                background: #2d2d2d;
                margin: 0;
                padding: 0;
            }
            QTableView { 
                background: #404040; 
                color: #ffffff;
                gridline-color: #555555;
                font-size: 14px;
                border: 1px solid #555555;
            }
            QHeaderView::section { 
                background: #505050; 
                color: #ffffff; 
                padding: 15px;
                font-size: 14px;
                border: 0;
            }
            QTabWidget::pane { 
                border: 0; 
                margin: 0;
                padding: 0;
                background: #404040;
            }
            QTabBar::tab {
                background: #353535;
                color: #aaaaaa;
                padding: 10px 25px;
                border: 1px solid #555555;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected { 
                background: #505050; 
                color: #ffffff;
                border-bottom-color: #505050;
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
            ("🗑️ Удалить", self.delete_selected),
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
        self.client_table = self.create_table(["Имя", "Телефон", "Email"])
        self.tour_table = self.create_table(["Направление", "Дата", "Цена", "Оператор"])
        self.order_table = self.create_table(["Клиент", "Тур", "Статус"])
        self.stats_tab = self.create_stats_tab()

        self.tabs.addTab(self.client_table, "Клиенты")
        self.tabs.addTab(self.tour_table, "Туры")
        self.tabs.addTab(self.order_table, "Заказы")
        self.tabs.addTab(self.stats_tab, "📊 Статистика")

    def create_table(self, headers):
        table = QTableView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        vertical_header = table.verticalHeader()
        vertical_header.setVisible(True)
        vertical_header.setDefaultSectionSize(40)
        vertical_header.setFixedWidth(50)
        vertical_header.setStyleSheet("""
            QHeaderView::section { 
                background: #3498db; 
                color: #ffffff;
                border: 0;
            }
        """)

        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setStyleSheet("border: 1px solid #dddddd;")

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
        chart.setBackgroundBrush(QColor("#ffffff"))

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
        for i, client in enumerate(self.session.query(Client).all()):
            model.appendRow([
                QStandardItem(client.name),
                QStandardItem(client.phone),
                QStandardItem(client.email or "")
            ])
            model.setData(model.index(i, 0), client.id, Qt.UserRole)

        # Туры
        model = self.tour_table.model()
        model.setRowCount(0)
        for i, tour in enumerate(self.session.query(Tour).all()):
            model.appendRow([
                QStandardItem(tour.destination),
                QStandardItem(tour.start_date.strftime("%d.%m.%Y")),
                QStandardItem(f"{tour.price} ₽"),
                QStandardItem(tour.operator or "")
            ])
            model.setData(model.index(i, 0), tour.id, Qt.UserRole)

        # Заказы
        model = self.order_table.model()
        model.setRowCount(0)
        for i, order in enumerate(self.session.query(Order).join(Client).join(Tour).all()):
            model.appendRow([
                QStandardItem(order.client.name),
                QStandardItem(order.tour.destination),
                QStandardItem(order.status)
            ])
            model.setData(model.index(i, 0), order.id, Qt.UserRole)

    def delete_selected(self):
        current_tab = self.tabs.currentIndex()
        table = None
        model_class = None

        if current_tab == 0:
            table = self.client_table
            model_class = Client
        elif current_tab == 1:
            table = self.tour_table
            model_class = Tour
        elif current_tab == 2:
            table = self.order_table
            model_class = Order

        if table and model_class:
            selected = table.selectionModel().selectedRows()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
                return

            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Удалить выбранные записи?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                try:
                    for index in reversed(selected):
                        row = index.row()
                        item_id = table.model().index(row, 0).data(Qt.UserRole)
                        record = self.session.query(model_class).get(item_id)
                        if record:
                            self.session.delete(record)
                    self.session.commit()
                    self.load_data()
                except Exception as e:
                    self.session.rollback()
                    QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")

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