import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from views import MainWindow
from database import Database


def apply_styles(app):
    app.setFont(QFont("Arial Black", 10))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_styles(app)

    db = Database()
    window = MainWindow(db.session)
    window.show()
    sys.exit(app.exec_())