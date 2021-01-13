# Importing libraries and files
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QTableWidgetItem
from main import Ui_MainWindow
import os, sys, qdarkstyle, mysql.connector, socket
from time import sleep

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
        self.ui.tabWidget_2.setVisible(False)
        self.ui.login_btn.clicked.connect(self.Handel_login)
        self.ui.feedback_btn.clicked.connect(self.client_program)
        self.ui.category_combo0.currentTextChanged.connect(self.show_test_info)

    # Handle patient login
    def Handel_login(self):
        username = self.ui.user_enter.text()
        password = self.ui.pass_enter.text()
        cur.execute(''' SELECT * FROM patients ''')
        data = cur.fetchall()
        patient = 0
        for i in range(0, len(data)):
            if username == data[i][1] and password == data[i][3]:
                patient = data[i][0]
                self.ui.tabWidget.setVisible(True)
                self.ui.tabWidget_2.setVisible(True)
                self.ui.user_enter.setText('')
                self.ui.pass_enter.setText('')
                self.show_records(patient)
                self.show_records_combobox()
                self.ui.login_failed.setText('Welcome ' + username)
                break
            else:
                self.ui.login_failed.setText('Make sure you entered your username and password correctly')

    # Records
    def show_records(self, patient):
        cur.execute(''' SELECT RBC, WBC, Hgb, Hematocrit, Platelets FROM records FULL JOIN patients ON p_id = %s order by p_id desc limit 1 ''' 
                                    % (patient))
        data = cur.fetchall()
        normal_ranges = [('4 - 5.2', '4 - 11', '12 - 16', '38.8 - 50', '150 - 450')]
        if data:
            self.ui.records_table.setRowCount(0)
            self.ui.records_table.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.ui.records_table.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.ui.records_table.rowCount()
                self.ui.records_table.insertRow(row_position)
            self.ui.records_table.setRowCount(1)
            self.ui.records_table.insertRow(0)
            for row, form in enumerate(normal_ranges):
                for column, item in enumerate(form):
                    self.ui.records_table.setItem(row, column, QTableWidgetItem(str(item)))
                    self.ui.records_table.item(row, column).setBackground(QtGui.QColor(100, 100, 150))
                    column += 1
                row_position = self.ui.records_table.rowCount()
                self.ui.records_table.insertRow(row_position)
    def show_records_combobox(self):
        data = ['RBC', 'WBC', 'Hgb', 'Hematocrit', 'Platelets']
        # print(data)
        for category in data:
            self.ui.category_combo0.addItem(category)

    def show_test_info(self):
        self.ui.Test_2.setEnabled(True)
        self.ui.Feedback_2.setEnabled(True)
        self.ui.Treatment.setEnabled(True)
        self.ui.treatment.setText('')
        self.ui.result.setText('')
        if self.ui.category_combo0.currentText() == 'RBC':
            self.ui.test.setText('A red blood cell (RBC) count is a blood test that your doctor uses to find out how many red blood cells (RBCs) you have.' + 
                                ' It’s also known as an erythrocyte count. The test is important because RBCs contain hemoglobin, which carries oxygen to your body’s tissues.' +
                                ' The number of RBCs you have can affect how much oxygen your tissues receive. Your tissues need oxygen to function.')
        if self.ui.category_combo0.currentText() == 'WBC':
            self.ui.test.setText('A white blood cell (WBC) count is a test that measures the number of white blood cells in your body.' +
                                ' This test is often included with a complete blood count (CBC). The term “white blood cell count” is also used more generally to refer to the number of white blood cells in your body.' +
                                ' There are several types of white blood cells, and your blood usually contains a percentage of each type. Sometimes, however, your white blood cell count can fall or rise out of the healthy range.')
        if self.ui.category_combo0.currentText() == 'Hgb':
            self.ui.test.setText('The hemoglobin (Hgb) test measures how much hemoglobin your red blood cells contain. Hgb is a protein produced by your bone marrow that’s stored in red blood cells.' +
                                ' It helps red blood cells transport oxygen from your lungs to your body through your arteries. It also transports carbon dioxide (CO2) from around your body back to your lungs through your veins. Hgb is what makes red blood cells look red.' +
                                ' Abnormally high or low Hgb can cause symptoms like exhaustion, dizziness, or shortness of breath. Your doctor may suggest an Hgb test if you’re experiencing these symptoms. You may have an underlying condition that needs to be diagnosed.')
        if self.ui.category_combo0.currentText() == 'Hematocrit':
            self.ui.test.setText('Hematocrit is the percentage of red blood cells in the total blood volume. Red blood cells are vital to your health.' +
                                ' Imagine them as the subway system of your blood. They transport oxygen and nutrients to various locations in your body. For you to stay healthy, your body needs to have the correct proportion of red blood cells.')
        if self.ui.category_combo0.currentText() == 'Platelets':
            self.ui.test.setText('A platelet aggregation test checks how well your platelets clump together to form blood clots. Platelets are a type of blood cell.' +
                                ' They help form blood clots by sticking together. A clot is what stops the bleeding when you have a wound. Without platelets, you could bleed to death. A platelet aggregation test requires a blood sample.' +
                                ' The sample is initially examined to see how the platelets are distributed through the plasma, the liquid part of the blood. A chemical is then added to your blood sample to test how quickly your platelets clot.')
        if self.ui.category_combo0.currentText() == 'Select Test':
            self.ui.test.setText('')
            self.ui.Test_2.setEnabled(False)
            self.ui.Feedback_2.setEnabled(False)
            self.ui.Treatment.setEnabled(False)

    # Socket Connection
    def client_program(self):
        # self.connect()
        # configure socket and connect to server  
        clientSocket = socket.socket()  
        host = socket.gethostname()  
        port = 25000  
        clientSocket.connect((host, port))
        self.statusBar().showMessage('Connection is established successfully')        
        # keep track of connection status  
        connected = True
        data = self.ui.record_enter.text()  # take input
        
        while True:
            # attempt to send and receive wave, otherwise reconnect  
            try:
                clientSocket.send(bytes(self.ui.category_combo0.currentText() + ' ' + data, "UTF-8"))
                message = clientSocket.recv(1024).decode("UTF-8")
                print(message)
                break
            except socket.error:  
                # set connection status and recreate socket  
                connected = False  
                clientSocket = socket.socket()  
                print( "connection lost... reconnecting" )  
                while not connected:  
                    # attempt to reconnect, otherwise sleep for 2 seconds  
                    try:  
                        clientSocket.connect((host, port))
                        connected = True  
                        print( "re-connection successful" )  
                    except socket.error:  
                        sleep( 2 )

        self.ui.record_enter.setText('')
        self.ui.result.setText('Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + message)
        self.suggest_treatment(self.ui.result.toPlainText())
        clientSocket.close()

    def suggest_treatment(self, treatment):
        # For all
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'You are in the normal range!':
            self.ui.treatment.setText('Just keep your healthy life :)')
        # RBC
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'Low RBC value!':
            self.ui.treatment.setText('You have Low RBC. So, Try to eat enough (folic acid), consumem more (Vitamin A), eat more Iron-Rich foods and the last thing is exercise Daily!')
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'High RBC value!':
            self.ui.treatment.setText('You have High RBC. So, Try phlebotomy or take medication for blood clot prevention!')
        # WBC
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'Low WBC value!':
            self.ui.treatment.setText('You have Low WBC. So, Avoid situations that expose you to infectious and contagious diseases and immunocompromised diet, try healthy food!')
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'High WBC value!':
            self.ui.treatment.setText('You have High WBC. So, Take antibiotics.')
        # Hgb
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'Low Hgb value!':
            self.ui.treatment.setText('You have Low Hgb. So, Increasing iron intake will be a good choice for you!')
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'High Hgb value!':
            self.ui.treatment.setText('You have High Hgb. So, Seek a doctor immediately!')
        # Hematocrit
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'Low Hematocrit value!':
            self.ui.treatment.setText('You have Low Hematocrit. So, You may require intravenous iron, transfusions or medications to stimulate the production of red cells by the bone narrow!')
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'High Hematocrit value!':
            self.ui.treatment.setText('You have High Hematocrit. So, You may require blood letting!')
        # Platelets
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'Low Platelets value!':
            self.ui.treatment.setText('You have Low Platelets. So, Try platelet transfusions!')
        if treatment == 'Feedback for ' + self.ui.category_combo0.currentText() + ' Test is: ' + 'High Platelets value!':
            self.ui.treatment.setText('You have High Platelets. So, Try taking aspirin!')

# Main Application to be run
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()