from PySide6 import QtWidgets, QtCore, QtGui
import time
import threading
import random

QUESTION = ["tkinter", 
            "geometry", 
            "widgets", 
            "messagebox", 
            "configure", 
            "label", 
            "column", 
            "rowspan", 
            "grid", 
            "init"]

class Application(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.index = 0
        self.correct_cnt = 0
        self.timer_thread = None  # タイマースレッドを管理する変数を追加

        self.create_widgets()
        self.shuffle_questions()  # 問題をシャッフルする

        self.start_timer_thread()  # タイマースレッドを開始する

    def shuffle_questions(self):
        random.shuffle(QUESTION)

    def create_widgets(self):
        layout = QtWidgets.QGridLayout()
        
        # 問題数を表示するラベル
        self.current_question_label = QtWidgets.QLabel()
        self.update_question_label()
        layout.addWidget(self.current_question_label, 0, 0, 1, 2)

        # 画像を表示する QLabel を作成し、画像をセットする
        pixmap = QtGui.QPixmap("assets/Typing Party.png")
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, 1, 0, 1, 2)

        self.q_label = QtWidgets.QLabel("お題：")
        self.q_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.q_label, 2, 0)

        self.q_label2 = QtWidgets.QLabel(QUESTION[self.index])
        self.q_label2.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.q_label2, 2, 1)

        self.ans_label = QtWidgets.QLabel("解答：")
        self.ans_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.ans_label, 3, 0)

        self.ans_label2 = QtWidgets.QLabel("")
        self.ans_label2.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.ans_label2, 3, 1)

        self.result_label = QtWidgets.QLabel("")
        self.result_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.result_label, 4, 0, 1, 2)

        self.time_label = QtWidgets.QLabel("")
        self.time_label.setFont(QtGui.QFont("", 20))  # Modify here
        layout.addWidget(self.time_label, 5, 0, 1, 2)

        # 再スタートボタンを作成し、クリックイベントを関連付ける
        restart_button = QtWidgets.QPushButton("再スタート")
        restart_button.setFont(QtGui.QFont("", 20))
        restart_button.clicked.connect(self.restart_game)
        layout.addWidget(restart_button, 6, 0, 1, 2)

        self.setLayout(layout)

    def restart_game(self):
        if self.timer_thread:  # タイマースレッドが存在する場合のみ処理する
            self.flg = False  # ループフラグを更新してタイマースレッドを終了させる
            self.timer_thread.join()  # スレッドが完全に終了するまで待機する
            self.timer_thread = None  # タイマースレッドを None に設定してリセットする
        self.index = 0
        self.correct_cnt = 0
        self.shuffle_questions()
        self.q_label2.setText(QUESTION[self.index])
        self.result_label.clear()
        
        # 新しいゲームを始めるときにタイマーをクリアしてから再スタートする
        self.time_label.clear()
        self.second = 0
        self.start_timer_thread()  # 新しいタイマースレッドを開始する
        self.current_question_label.setText(f"現在の問題数：{self.index + 1}/{len(QUESTION)}")

    def update_question_label(self):
        self.current_question_label.setText(f"現在の問題数：{self.index + 1}/{len(QUESTION)}")

    def start_timer_thread(self):
        t = threading.Thread(target=self.timer)
        t.start()
        self.timer_thread = t  # 新しいタイマースレッドを保存しておく

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
                QtWidgets.QMessageBox.information(self, "結果発表！", f"あなたのスコアは{self.correct_cnt}/{self.index}問正解です。\nクリアタイムは{self.second}秒です。おめでとうございます！")
                QtCore.QCoreApplication.quit()

            self.q_label2.setText(QUESTION[self.index])
            self.update_question_label()

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