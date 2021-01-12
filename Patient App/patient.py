# Importing libraries and files
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QIcon
from main import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import cv2 as cv
import sys, qdarkstyle, mysql.connector, socket

# ui,_ = loadUiType('patient_design.ui')
# login,_ = loadUiType('login.ui')
db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'DARSH1999', db = 'laboratory')
cur = db.cursor()

# class login(QWidget, login):
#     def __init__(self):
#         QWidget.__init__(self)
#         self.setupUi(self)
#         self.login_btn.clicked.connect(self.Handel_login)

#     def Handel_login(self):
#         username = self.user_enter.text()
#         password = self.pass_enter.text()
#         cur.execute(''' SELECT * FROM patients ''')
#         data = cur.fetchall()
#         patient = 0
#         for i in range(0, len(data)):
#             if username == data[i][1] and password == data[i][3]:
#                 patient = data[i][0]
#                 self.window2 = MainApp()
#                 self.show_records(patient)
#                 self.close()
#                 self.window2.show()
#             else:
#                 self.login_failed.setText('Make sure you entered your username and password correctly')

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabWidget.setVisible(False)
        self.ui.login_btn.clicked.connect(self.Handel_login)
        self.ui.feedback_btn.clicked.connect(self.client_program)

    def Handel_login(self):
        username = self.ui.user_enter.text()
        password = self.ui.pass_enter.text()
        cur.execute(''' SELECT * FROM patients ''')
        data = cur.fetchall()
        patient = 0
        for i in range(0, len(data)):
            if username == data[i][1] and password == data[i][3]:
                patient = data[i][0]
                self.ui.tabWidget.setVisible(True) # .tabBar().setVisible(False)
                # self.ui.tabWidget.setCurrentIndex(0)
                self.show_records(patient)
            else:
                self.ui.login_failed.setText('Make sure you entered your username and password correctly')

    # Records
    def show_records(self, patient):
        cur.execute(''' SELECT RBC, WBC, Hgb, PCV, Platelets FROM records FULL JOIN patients ON p_id = %s '''
                                    % (patient))
        data = cur.fetchall()
        print(data)
        if data:
            self.ui.records_table.setRowCount(0)
            self.ui.records_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.records_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ui.records_table.rowCount()
                self.ui.records_table.insertRow(row_position)

    # Socket Connection
    def client_program(self):
        host = socket.gethostname()  # as both code is running on same pc
        port = 5000  # socket server port number

        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server

        message = self.ui.record_enter.text()  # take input

        while message.lower().strip() != 'bye':
            print(message)
            client_socket.send(message.encode())  # send message
            data = client_socket.recv(1024).decode()  # receive response
            print('Received from server: ' + data)  # show in terminal
            self.ui.result.setText(data)
        
        message = self.ui.record_enter.text()  # again take input

        client_socket.close()  # close the connection

# Main Application to be run
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()