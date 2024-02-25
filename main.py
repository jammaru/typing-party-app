from PySide6 import QtWidgets
from application import Application

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Application()
    window.setWindowTitle("タイピング パーティー！")
    window.setGeometry(100, 100, 300, 200)
    window.show()
    app.exec()
