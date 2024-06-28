import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import subprocess


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Database Table Selector')
        self.setGeometry(100, 100, 300, 200)

        # 创建按钮并设置位置
        btnS = QPushButton('S表', self)
        btnS.move(50, 50)
        btnS.clicked.connect(lambda: self.openTable('S.py'))

        btnCla = QPushButton('Cla表', self)
        btnCla.move(50, 100)
        btnCla.clicked.connect(lambda: self.openTable('Cla.py'))

        btnCou = QPushButton('Cou表', self)
        btnCou.move(50, 150)
        btnCou.clicked.connect(lambda: self.openTable('Cou.py'))

    def openTable(self, script):
        # 使用 subprocess 运行对应的 Python 脚本文件
        subprocess.Popen([sys.executable, script])
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())