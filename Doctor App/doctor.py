# Importing libraries and files
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from main import Ui_MainWindow
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
        self.ui.add_patient.clicked.connect(self.Add_patient)
        self.ui.edit_patient.clicked.connect(self.Edit_patient)
        self.ui.add_record.clicked.connect(self.Add_record)

    # Handel doctor login
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

    # Patients
    def Show_patient_info(self):
        cur.execute(''' SELECT * From patients ''')
        data = cur.fetchall()
        if data:
            self.ui.patient_table_2.setRowCount(0)
            self.ui.patient_table_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.patient_table_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position_2 = self.ui.patient_table_2.rowCount()
                self.ui.patient_table_2.insertRow(row_position_2)
    def Add_patient(self):
        p_id = self.ui.p_id.text()
        p_name = self.ui.p_name.text()
        p_email = self.ui.p_mail.text()
        p_pass = self.ui.p_pass.text()
        if p_id == '' or p_name == '' or p_email == '' or p_pass == '':
            self.statusBar().showMessage('You have an empty field, please re-check!')
        else:
            cur.execute(''' INSERT INTO patients (patient_id, patient_name, patient_email, patient_password) VALUES (%s, %s, %s, %s) '''
                            , (p_id, p_name, p_email, p_pass))
            db.commit()
            self.statusBar().showMessage('New Patient Added')
            self.Show_patient_info()
            self.ui.p_id.setText('')
            self.ui.p_name.setText('')
            self.ui.p_mail.setText('')
            self.ui.p_pass.setText('')
    def Edit_patient(self):
        p_id = self.ui.p_id_2.text()
        p_name = self.ui.p_name_2.text()
        p_email = self.ui.p_mail_2.text()
        p_pass = self.ui.p_pass_2.text()
        if p_id == '' or p_name == '' or p_email == '' or p_pass == '':
            self.statusBar().showMessage('You have an empty field, please re-check!')
        else:
            cur.execute(''' UPDATE patients SET patient_id = %s, patient_name = %s, patient_email = %s, patient_password = %s WHERE patient_id = %s '''
                            , (p_id, p_name, p_email, p_pass, p_id))
            db.commit()
            self.statusBar().showMessage('Edited patient successfully')
            self.Show_patient_info()
            self.ui.p_id_2.setText('')
            self.ui.p_name_2.setText('')
            self.ui.p_mail_2.setText('')
            self.ui.p_pass_2.setText('')

    # Records
    def Show_record_info(self):
        cur.execute(''' SELECT * From records ''')
        data = cur.fetchall()
        if data:
            self.ui.record_table_2.setRowCount(0)
            self.ui.record_table_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.record_table_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position_2 = self.ui.record_table_2.rowCount()
                self.ui.record_table_2.insertRow(row_position_2)
    def Add_record(self):
        RBC = self.ui.RBC.text()
        WBC = self.ui.WBC.text()
        Hgb = self.ui.Hgb.text()
        Hematocrit = self.ui.Hematocrit.text()
        Platelets = self.ui.Platelets.text()
        pr_id = self.ui.pr_id.text()
        if RBC == '' or WBC == '' or Hgb == '' or Hematocrit == '' or Platelets == '' or pr_id == '':
            self.statusBar().showMessage('You have an empty field, please re-check!')
        else:
            cur.execute(''' INSERT INTO records (RBC, WBC, Hgb, Hematocrit, Platelets, p_id) VALUES (%s, %s, %s, %s, %s, %s) '''
                            , (RBC, WBC, Hgb, Hematocrit, Platelets, pr_id))
            db.commit()
            self.statusBar().showMessage('New Record Added')
            self.Show_record_info()
            self.ui.RBC.setText('')
            self.ui.WBC.setText('')
            self.ui.Hgb.setText('')
            self.ui.Hematocrit.setText('')
            self.ui.Platelets.setText('')
            self.ui.pr_id.setText('')

    # Doctor
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