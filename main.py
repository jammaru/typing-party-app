from PySide6 import QtWidgets
from application import Application

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Application()
    window.setWindowTitle("タイピング パーティー！")
    window.setFixedSize(300, 200)  # サイズ固定
    window.setMaximumSize(300, 200)  # 最大サイズを設定して最大化を禁止
    window.setGeometry(100, 100, 300, 200)
    window.show()
    app.exec()
