import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QRadioButton, QLabel
import psycopg2
import subprocess

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建布局和控件
        layout = QVBoxLayout()
        self.resize(800, 600)
        self.admin_radio = QRadioButton('管理员登录')
        self.user_radio = QRadioButton('用户登录')
        self.username_line = QLineEdit( )
        self.password_line = QLineEdit( )
        self.password_line.setEchoMode(QLineEdit.EchoMode.Password)  # 修正这里

        # 仅当选择管理员登录时显示用户名和密码输入框
        self.username_line.setVisible(False)
        self.password_line.setVisible(False)

        self.admin_radio.toggled.connect(self.on_admin_toggled)
        self.user_radio.toggled.connect(self.on_user_toggled)

        login_button = QPushButton('登录')
        login_button.clicked.connect(self.on_login)

        layout.addWidget(self.admin_radio)
        layout.addWidget(self.user_radio)
        layout.addWidget(self.username_line)
        layout.addWidget(self.password_line)
        layout.addWidget(login_button)

        self.setLayout(layout)
        self.setWindowTitle('学校信息管理系统')
        self.show()

    def on_admin_toggled(self, state):
        if state:
            self.username_line.setVisible(True)
            self.password_line.setVisible(True)

    def on_user_toggled(self, state):
        if state:
            self.username_line.setVisible(False)
            self.password_line.setVisible(False)

    def on_login(self):
        if self.admin_radio.isChecked():
            # 管理员登录验证逻辑（这里只是示例，你需要实现真正的验证）
            username = self.username_line.text()
            password = self.password_line.text()
            if username == 'hsj' and password == '123456789':  # 示例验证条件
                print("管理员登录成功！")
                subprocess.Popen([sys.executable, "管理员操作界面.py"])
            else:
                print("用户名或密码错误！")
        elif self.user_radio.isChecked():
            subprocess.Popen([sys.executable, "用户查看界面.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec())