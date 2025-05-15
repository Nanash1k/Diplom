from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QTableView, QLabel, QPushButton, QHBoxLayout,
    QHeaderView, QAbstractItemView, QToolBar, QAction,
    QMessageBox, QSizePolicy, QStyledItemDelegate, QLineEdit
)
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QDate
from PyQt5.QtGui import (QPainter, QStandardItemModel, QStandardItem,
                         QColor, QFont, QPalette, QBrush)
from database import Client, Tour, Order
from widgets.client_form import ClientForm
from widgets.tour_form import TourForm
from widgets.order_form import OrderForm
from sqlalchemy import func


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(160, 48)
        self.setCursor(Qt.PointingHandCursor)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)

    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self._animation.start()
        super().leaveEvent(event)


class TableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            editor.setStyleSheet("""
                QLineEdit {
                    background: #404040;
                    color: white;
                    border: 2px solid #6a1b9a;
                    margin: -1px;
                    padding: 0;
                }
            """)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect.adjusted(-2, 0, 2, 0))

class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("ТурМенеджер PRO")
        self.setMinimumSize(1400, 900)
        self.setup_style()
        self.setup_toolbar()
        self.setup_tabs()

    def setup_style(self):
        self.setStyleSheet("""
            QMainWindow { background: #2d2d2d; }
            QTabWidget::pane {
                border: 0;
                background: #363636;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #444;
                color: #ddd;
                min-width: 120px;
                padding: 12px;
                border: 0;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #6a1b9a;
                color: white;
            }
        """)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(15)

    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7b1fa2, stop:1 #6a1b9a);
                color: white;
                border-radius: 6px;
                padding: 10px;
                margin: 2px;
            }
            QToolButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #8e24aa, stop:1 #7b1fa2);
            }
        """)
        buttons = [
            ("➕ Добавить клиента", self.open_client_form),
            ("✈️ Создать тур", self.open_tour_form),
            ("📦 Новый заказ", self.open_order_form),
            ("🗑️ Удалить выбранное", self.delete_selected),
            ("🔄 Обновить данные", self.load_data)
        ]
        for text, callback in buttons:
            btn = AnimatedButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: white;
                    font-weight: 500;
                    border: 2px solid #7b1fa2;
                    border-radius: 6px;
                }
                QPushButton:hover { background: #7b1fa255; }
            """)
            btn.clicked.connect(callback)
            toolbar.addWidget(btn)
        self.centralWidget().layout().addWidget(toolbar)

    def setup_tabs(self):
        self.tabs = QTabWidget()
        self.client_table = self.create_table(["Имя", "Телефон", "Email", "Паспорт"])
        self.tour_table = self.create_table(["Направление", "Дата", "Цена", "Оператор", "Взрослые", "Дети"])
        self.order_table = self.create_table(["Клиент", "Тур", "Статус"])
        self.stats_tab = self.create_stats_tab()

        self.tabs.addTab(self.client_table, "👤 Клиенты")
        self.tabs.addTab(self.tour_table, "🌍 Туры")
        self.tabs.addTab(self.order_table, "📦 Заказы")
        self.tabs.addTab(self.stats_tab, "📊 Аналитика")
        self.centralWidget().layout().addWidget(self.tabs)

    def create_table(self, headers):
        table = QTableView()
        table.setStyleSheet("""
            QTableView {
                background: #404040;
                color: white;
                border: 1px solid #555;
                gridline-color: #555;
                selection-background-color: #6a1b9a;
                selection-color: white;
            }
            QTableView::item {
                background: #404040;
                color: white;
                border: none;
                padding: 8px;
            }
            QTableView::item:selected { background: #6a1b9a; }
            QHeaderView::section {
                background: #6a1b9a;
                color: white;
                padding: 10px;
                border: 0;
            }
        """)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        table.setModel(model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.verticalHeader().hide()
        table.setEditTriggers(QTableView.DoubleClicked)
        table.setItemDelegate(TableDelegate())
        return table

    def create_stats_tab(self):
        tab = QWidget()
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        tab.setLayout(layout)
        self.update_stats()
        return tab

    def update_stats(self):
        series = QPieSeries()
        tours = self.session.query(
            Tour.destination,
            func.count(Order.id).label('order_count')
        ).outerjoin(Order).group_by(Tour.id).all()

        colors = [QColor("#9C27B0"), QColor("#2196F3"), QColor("#4CAF50"),
                  QColor("#FF9800"), QColor("#E91E63"), QColor("#00BCD4")]

        for i, (destination, count) in enumerate(tours):
            if count == 0: continue
            slice_ = QPieSlice(f"{destination} ({count})", count)
            slice_.setColor(colors[i % len(colors)])
            series.append(slice_)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Распределение заказов по турам")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QBrush(QColor(64, 64, 64)))
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setChart(chart)

    def load_data(self):
        # Клиенты
        model = self.client_table.model()
        model.setRowCount(0)
        for client in self.session.query(Client).all():
            items = [
                self.create_white_item(client.name),
                self.create_white_item(client.phone),
                self.create_white_item(client.email or ""),
                self.create_white_item(client.passport or "")
            ]
            model.appendRow(items)

        # Туры
        model = self.tour_table.model()
        model.setRowCount(0)
        for tour in self.session.query(Tour).all():
            items = [
                self.create_white_item(tour.destination),
                self.create_white_item(tour.start_date.strftime("%d.%m.%Y")),
                self.create_white_item(f"{tour.price} ₽"),
                self.create_white_item(tour.operator or "-"),
                self.create_white_item(str(tour.adults)),
                self.create_white_item(str(tour.children))
            ]
            model.appendRow(items)

        # Заказы
        model = self.order_table.model()
        model.setRowCount(0)
        for order in self.session.query(Order).join(Client).join(Tour).all():
            items = [
                self.create_white_item(order.client.name),
                self.create_white_item(order.tour.destination),
                self.create_white_item(order.status)
            ]
            model.appendRow(items)
        self.update_stats()

    def create_white_item(self, text):
        item = QStandardItem(text)
        item.setForeground(QColor(255, 255, 255))
        return item

    def open_client_form(self):
        form = ClientForm(self)
        if form.exec_():
            self.session.add(Client(
                name=form.name_input.text(),
                phone=form.phone_input.text(),
                email=form.email_input.text(),
                passport=form.passport_input.text()
            ))
            self.session.commit()
            self.load_data()

    def open_tour_form(self):
        form = TourForm(self)
        if form.exec_():
            self.session.add(Tour(
                destination=form.destination_input.text(),
                operator=form.operator_input.text(),
                start_date=form.date_input.date().toPyDate(),
                duration=form.duration_input.value(),
                price=form.price_input.value(),
                adults=form.adults_input.value(),
                children=form.children_input.value()
            ))
            self.session.commit()
            self.load_data()

    def open_order_form(self):
        form = OrderForm(self.session, self)
        if form.exec_():
            client_id = form.client_combo.currentData()
            tour_id = form.tour_combo.currentData()
            status = form.status_combo.currentText()

            new_order = Order(
                client_id=client_id,
                tour_id=tour_id,
                status=status
            )
            self.session.add(new_order)
            self.session.commit()
            self.load_data()

    def delete_selected(self):
        current_tab = self.tabs.currentIndex()
        table = None
        model_class = None
        entity_name = ""

        if current_tab == 0:
            table = self.client_table
            model_class = Client
            entity_name = "клиента"
        elif current_tab == 1:
            table = self.tour_table
            model_class = Tour
            entity_name = "тур"
        elif current_tab == 2:
            table = self.order_table
            model_class = Order
            entity_name = "заказ"

        if table and model_class:
            selected = table.selectionModel().selectedRows()
            if not selected:
                msg = QMessageBox()
                msg.setStyleSheet("""
                    QMessageBox {
                        background: #404040;
                        color: #fff;
                    }
                    QLabel {
                        color: #fff;
                        font: 14px;
                    }
                    QPushButton {
                        background: #6a1b9a;
                        color: white;
                        min-width: 80px;
                        padding: 8px;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background: #7b1fa2;
                    }
                """)
                msg.setWindowTitle("Ошибка")
                msg.setText("Выберите запись для удаления")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                return

            count = len(selected)
            message = QMessageBox()
            message.setStyleSheet("""
                QMessageBox {
                    background: #404040;
                    color: #fff;
                }
                QLabel {
                    color: #fff;
                    font: 14px;
                }
                QPushButton {
                    background: #6a1b9a;
                    color: white;
                    min-width: 80px;
                    padding: 8px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #7b1fa2;
                }
            """)
            message.setWindowTitle("Подтверждение удаления")
            message.setText(
                f"Вы действительно хотите удалить {count} {self.declension(entity_name, count)}?\n\n"
                "* Это действие нельзя будет отменить!"
            )
            message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message.setDefaultButton(QMessageBox.No)

            if message.exec_() == QMessageBox.Yes:
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
                    error_box = QMessageBox()
                    error_box.setStyleSheet("""
                        QMessageBox {
                            background: #404040;
                            color: #fff;
                        }
                        QLabel {
                            color: #ff4444;
                            font: bold 14px;
                        }
                        QPushButton {
                            background: #6a1b9a;
                            color: white;
                            min-width: 80px;
                            padding: 8px;
                            border-radius: 4px;
                        }
                    """)
                    error_box.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")

    def declension(self, word, number):
        variants = {
            "клиента": ["клиент", "клиента", "клиентов"],
            "тур": ["тур", "тура", "туров"],
            "заказ": ["заказ", "заказа", "заказов"]
        }
        cases = [2, 0, 1, 1, 1, 2]
        if 4 < number % 100 < 20:
            return variants[word][2]
        else:
            return variants[word][cases[min(number % 10, 5)]]