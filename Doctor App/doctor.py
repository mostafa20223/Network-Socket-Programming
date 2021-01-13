# Importing libraries and files
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon, QBrush, QColor
from main import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import cv2 as cv
import sys, qdarkstyle, mysql.connector, socket

# Connect to database
db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'DARSH1999', db = 'laboratory')
cur = db.cursor()

# Start the app
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabWidget.setVisible(False)
        self.ui.login_btn.clicked.connect(self.Handel_login)

    def Handel_login(self):
        username = self.ui.user_enter.text()
        password = self.ui.pass_enter.text()
        cur.execute(''' SELECT * FROM doctor ''')
        data = cur.fetchall()
        ID = 0
        for i in range(0, len(data)):
            if username == data[i][1] and password == data[i][2]:
                self.ui.tabWidget.setVisible(True)
                self.ui.login_failed.setText('Welcome ' + username)
                self.ui.user_enter.setText('')
                self.ui.pass_enter.setText('')
                ID = data[i][0]
                self.Show_doctor_info(ID)
                self.Show_patient_info()
                self.Show_record_info()
                break
            else:
                self.ui.login_failed.setText('Make sure you entered your username and password correctly')

    def Show_patient_info(self):
        cur.execute(''' SELECT * From patients ''')
        data = cur.fetchall()
        if data:
            self.ui.patient_table.setRowCount(0)
            self.ui.patient_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.patient_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ui.patient_table.rowCount()
                self.ui.patient_table.insertRow(row_position)

    def Show_record_info(self):
        cur.execute(''' SELECT * From records ''')
        data = cur.fetchall()
        if data:
            self.ui.record_table.setRowCount(0)
            self.ui.record_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.record_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ui.record_table.rowCount()
                self.ui.record_table.insertRow(row_position)

    def Show_doctor_info(self, ID):
        cur.execute(''' SELECT username, password, email From doctor WHERE id = %s '''
                            % (ID))
        data = cur.fetchall()
        if data:
            self.ui.doctor_table.setRowCount(0)
            self.ui.doctor_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.doctor_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ui.doctor_table.rowCount()
                self.ui.doctor_table.insertRow(row_position)

# Main Application to be run
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()