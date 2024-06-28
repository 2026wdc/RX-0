import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox
import psycopg2


class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(database="db_tpcc", user="joe", password="Bigdata@123", host="1.94.201.203",
                                     port="26000")
        self.cur = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cur.execute(query, params)
            self.conn.commit()
            return self.cur.fetchall()
        except Exception as e:
            self.conn.rollback()
            return str(e)

    def close(self):
        self.cur.close()
        self.conn.close()


class ClaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("班级信息表Cla")
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Form fields
        self.cno_input = QLineEdit()
        self.cteacher_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.number_input = QLineEdit()

        # Buttons
        insert_button = QPushButton("插入")
        query_button = QPushButton("查询")
        update_button = QPushButton("更新")
        delete_button = QPushButton("删除")

        # Table for displaying results
        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels(["Cno", "Cteacher", "Grade", "Number"])

        # Adding widgets to layouts
        form_layout.addWidget(QLabel("Cno:"))
        form_layout.addWidget(self.cno_input)
        form_layout.addWidget(QLabel("Cteacher:"))
        form_layout.addWidget(self.cteacher_input)
        form_layout.addWidget(QLabel("Grade:"))
        form_layout.addWidget(self.grade_input)
        form_layout.addWidget(QLabel("Number:"))
        form_layout.addWidget(self.number_input)

        button_layout.addWidget(insert_button)
        button_layout.addWidget(query_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.results_table)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Connect buttons to functions
        insert_button.clicked.connect(self.insert_data)
        query_button.clicked.connect(self.query_data)
        update_button.clicked.connect(self.update_data)
        delete_button.clicked.connect(self.delete_data)

    def insert_data(self):
        cno = self.cno_input.text()
        cteacher = self.cteacher_input.text()
        grade = self.grade_input.text()
        number = self.number_input.text()

        # Check if the record exists
        existing_records = self.db_manager.execute_query(
            "SELECT * FROM Cla WHERE Cno=%s AND Cteacher=%s AND Grade=%s AND Number=%s", (cno, cteacher, grade, number))

        if existing_records:
            QMessageBox.information(self, "Error", "这条记录已存在")
            return

        result = self.db_manager.execute_query("""
            INSERT INTO Cla (Cno, Cteacher, Grade, Number) VALUES (%s, %s, %s, %s);
            """, (cno, cteacher, grade, number))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Operation successful!")
            self.clear_inputs()

    def query_data(self):
        cno = self.cno_input.text()

        results = self.db_manager.execute_query("SELECT * FROM Cla WHERE Cno=%s", (cno,))

        if not results:
            QMessageBox.information(self, "Not Found", "No records found!")
            return

        self.results_table.setRowCount(0)  # Clear previous results

        for row_number, row_data in enumerate(results):
            self.results_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.results_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def update_data(self):
        cno = self.cno_input.text()
        cteacher = self.cteacher_input.text()
        grade = self.grade_input.text()
        number = self.number_input.text()

        result = self.db_manager.execute_query("""
            UPDATE Cla SET Cteacher=%s, Grade=%s, Number=%s WHERE Cno=%s;
            """, (cteacher, grade, number, cno))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Operation successful!")
            self.clear_inputs()

    def delete_data(self):
        cno = self.cno_input.text()

        result = self.db_manager.execute_query("DELETE FROM Cla WHERE Cno=%s", (cno,))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Operation successful!")
            self.clear_inputs()

    def clear_inputs(self):
        self.cno_input.clear()
        self.cteacher_input.clear()
        self.grade_input.clear()
        self.number_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClaWindow()
    window.show()
    sys.exit(app.exec())
