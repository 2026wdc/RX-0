import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QListWidget, QTableWidget, \
    QTableWidgetItem
import psycopg2

class TableSelector(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.initUI()

    def initUI(self):
        self.setWindowTitle('用户查看界面')
        self.setGeometry(200, 100, 800, 600)

        self.tableList = QListWidget()
        self.tableList.addItems(['S', 'Cla', 'Cou'])

        self.tableWidget = QTableWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableList)
        self.layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.tableList.itemClicked.connect(self.showTableData)

    def showTableData(self, item):
        table_name = item.text()
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(len(columns))
            self.tableWidget.setHorizontalHeaderLabels(columns)

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))


def main():
    app = QApplication(sys.argv)
    conn = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="1.94.201.203", port=26000)
    window = TableSelector(conn)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()