from PySide6 import QtWidgets, QtCore, QtGui
import sys
import time
import threading


QUESTION = ["tkinter", "geometry", "widgets", "messagebox", "configure", 
            "label", "column", "rowspan", "grid", "init"]

class Application(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.index = 0
        self.correct_cnt = 0

        self.create_widgets()

        t = threading.Thread(target=self.timer)
        t.start()

    def create_widgets(self):
        layout = QtWidgets.QGridLayout()

        self.q_label = QtWidgets.QLabel("お題：")
        self.q_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.q_label, 0, 0)

        self.q_label2 = QtWidgets.QLabel(QUESTION[self.index])
        self.q_label2.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.q_label2, 0, 1)

        self.ans_label = QtWidgets.QLabel("解答：")
        self.ans_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.ans_label, 1, 0)

        self.ans_label2 = QtWidgets.QLabel("")
        self.ans_label2.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.ans_label2, 1, 1)

        self.result_label = QtWidgets.QLabel("")
        self.result_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.result_label, 2, 0, 1, 2)

        self.time_label = QtWidgets.QLabel("")
        self.time_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.time_label, 3, 0, 1, 2)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if self.q_label2.text() == self.ans_label2.text():
                self.result_label.setText("正解！")
                self.result_label.setStyleSheet("color: red")
                self.correct_cnt += 1
            else:
                self.result_label.setText("残念！")
                self.result_label.setStyleSheet("color: blue")

            self.ans_label2.setText("")
            self.index += 1

            if self.index == len(QUESTION):
                self.flg = False
                self.q_label2.setText("終了！")
                QtWidgets.QMessageBox.information(self, "リザルト", f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。")
                sys.exit(0)

            self.q_label2.setText(QUESTION[self.index])

        elif event.key() == QtCore.Qt.Key_Backspace:
            text = self.ans_label2.text()
            self.ans_label2.setText(text[:-1])

        else:
            self.ans_label2.setText(self.ans_label2.text() + event.text())

    def timer(self):
        self.second = 0
        self.flg = True
        while self.flg:
            self.second += 1
            self.time_label.setText(f"経過時間：{self.second}秒")
            time.sleep(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.setWindowTitle("タイピングゲーム！")
    window.setGeometry(100, 100, 300, 200)
    window.show()
    sys.exit(app.exec())
