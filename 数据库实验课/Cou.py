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


class CouWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("学生选修课信息表Cou")
        self.setGeometry(100, 100, 900, 600)

        # Layouts
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Form fields
        self.sno_input = QLineEdit()
        self.sname_input = QLineEdit()
        self.cou1_input = QLineEdit()
        self.cou2_input = QLineEdit()
        self.cou3_input = QLineEdit()

        # Buttons
        insert_button = QPushButton("插入")
        query_button = QPushButton("查询")
        update_button = QPushButton("更新")
        delete_button = QPushButton("删除")

        # Table for displaying results
        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["Sno", "Sname", "Cou1", "Cou2", "Cou3"])

        # Adding widgets to layouts
        form_layout.addWidget(QLabel("Sno:"))
        form_layout.addWidget(self.sno_input)
        form_layout.addWidget(QLabel("Sname:"))
        form_layout.addWidget(self.sname_input)
        form_layout.addWidget(QLabel("Cou1:"))
        form_layout.addWidget(self.cou1_input)
        form_layout.addWidget(QLabel("Cou2:"))
        form_layout.addWidget(self.cou2_input)
        form_layout.addWidget(QLabel("Cou3:"))
        form_layout.addWidget(self.cou3_input)

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
        sno = self.sno_input.text()
        sname = self.sname_input.text()
        cou1 = self.cou1_input.text()
        cou2 = self.cou2_input.text()
        cou3 = self.cou3_input.text()

        # Check if the record with same Sno and Sname exists
        existing_records = self.db_manager.execute_query("SELECT * FROM Cou WHERE Sno=%s AND Sname=%s", (sno, sname))

        if existing_records:
            QMessageBox.information(self, "Error", "这名学生已经存在")
            return

        result = self.db_manager.execute_query("""
            INSERT INTO Cou (Sno, Sname, Cou1, Cou2, Cou3) VALUES (%s, %s, %s, %s, %s);
            """, (sno, sname, cou1, cou2, cou3))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Record inserted successfully!")
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Failed to insert record: " + str(result))

    def query_data(self):
        cou1 = self.cou1_input.text()
        cou2 = self.cou2_input.text()
        cou3 = self.cou3_input.text()

        query_parts = []
        params = []

        if cou1:
            query_parts.append("Cou1=%s")
            params.append(cou1)

        if cou2:
            query_parts.append("Cou2=%s")
            params.append(cou2)

        if cou3:
            query_parts.append("Cou3=%s")
            params.append(cou3)

        if not query_parts:
            QMessageBox.information(self, "Error", "Please enter at least one course to search.")
            return

        query_string = " AND ".join(query_parts)

        results = self.db_manager.execute_query(f"SELECT * FROM Cou WHERE {query_string}", tuple(params))

        if not results:
            QMessageBox.information(self, "Not Found", "No records found!")
            return

        self.results_table.setRowCount(0)  # Clear previous results

        for row_number, row_data in enumerate(results):
            self.results_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.results_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def update_data(self):
        sno = self.sno_input.text()
        sname = self.sname_input.text()
        cou1 = self.cou1_input.text()
        cou2 = self.cou2_input.text()
        cou3 = self.cou3_input.text()

        result = self.db_manager.execute_query("""
            UPDATE Cou SET Sname=%s, Cou1=%s, Cou2=%s, Cou3=%s WHERE Sno=%s;
            """, (sname, cou1, cou2, cou3, sno))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Operation successful!")
            self.clear_inputs()

    def delete_data(self):
        sno = self.sno_input.text()

        result = self.db_manager.execute_query("DELETE FROM Cou WHERE Sno=%s", (sno,))

        if isinstance(result, list):
            QMessageBox.information(self, "Success", "Operation successful!")
            self.clear_inputs()

    def clear_inputs(self):
        self.sno_input.clear()
        self.sname_input.clear()
        self.cou1_input.clear()
        self.cou2_input.clear()
        self.cou3_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CouWindow()
    window.show()
    sys.exit(app.exec())
