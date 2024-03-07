





import sys
import requests
import json

import warnings
from PIL import Image, ImageEnhance
warnings.filterwarnings('ignore')
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
from keras.preprocessing import image



from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QMainWindow,QVBoxLayout, QPushButton, QDialog, QFileDialog, QListWidget,QListWidgetItem,QTableWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QDesktopServices, QFont

class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        
        
        
       
        

    def initUI(self):
     
     # Create widgets
     goBackButton = QPushButton('GoBack', self)
     
     label = QLabel('Pneumonia is an infection that inflames your lungs air sacs (alveoli). The air sacs may fill up with fluid or pus, causing symptoms such as a cough, fever, chills and trouble breathing', self)
     label.setWordWrap(True)    
     openFileButton = QPushButton("Open File",self)
     predictButton =QPushButton("Predict", self)
     

     # print("patentname",self.patientName)

     # Connect button click signal to a custom function
     goBackButton.clicked.connect(self.goBack)
     goBackButton.setFixedSize(50, 50)

     openFileButton.clicked.connect(self.upload_image)
     predictButton.clicked.connect(self.predict_result)
     # Create layout and add widgets
     
     layout = QVBoxLayout(self)
     
     layout.addWidget(goBackButton)
     layout.addWidget(predictButton)
     layout.addWidget(label)

     
     layout.addWidget(openFileButton)

     # Set layout for the main window
     self.setLayout(layout)

     # Set window properties
     self.setWindowTitle('Home Page')
     self.setGeometry(100, 100, 400, 300)

    def goBack(self):
     widget.setCurrentIndex(2)
        
    def upload_image(self):
        filename= QFileDialog.getOpenFileName()
        # if not filename:
        #     print("not opened")
        #     return
        # else:
        path=filename[0]
        path=str(path)
        print(path)
        model=load_model('D:\\sem7\\project\\modelTrain1.h5') 
        print("Model:",model)
        img_file=image.load_img(path,target_size=(224,224))
        x=image.img_to_array(img_file)
        x=np.expand_dims(x, axis=0)
        x /= 255.0
        # img_data=preprocess_input(x)
        
        predictions=model.predict(x)
        
        global result
        result=predictions 
        print("result",result) 

    def predict_result(self):
        predicted_class_index = np.argmax(result)
        class_labels = ['Not Pneumonia', 'Pneumonia'] 
        
        predicted_class_label = class_labels[predicted_class_index]
        print(f'Predicted Class: {predicted_class_label}')
        
        if(predicted_class_label=='Pneumonia'):
            test = True
        else:
            test = False    

        send_data ={
            'user': username,
            'result': test,
            'patient':patientname,
            
        }
        apiEndpoint = "http://localhost:3000/api/patient/test"
        response = requests.post(apiEndpoint, json=send_data)
        data = response.json()
             
        resWidget = ResultDisplayWidget(predicted_class_label)
        widget.addWidget(resWidget)
        widget.setCurrentIndex(6)
        # if result[0][0]>0.5:
        #     print("Result is Normal")
        # else:
        #     print("Affected By PNEUMONIA")
    # def setPatientName(self, newPatientName):
        # self.patientName = newPatientName
        # self.patient.setText(newPatientName) 

class ResultDisplayWidget(QWidget):
    def __init__(self, text, parent=None):
        super(ResultDisplayWidget, self).__init__(parent)
        self.initUI(text)

    def initUI(self,text):
        # Create a vertical layout
        layout = QVBoxLayout()
        self.text = text
       
        # Create a label and set its properties for displaying results
        self.resultLabel = QLabel(patientname+" has "+self.text)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setFont(QFont("Arial", 16))
        self.resultLabel.setWordWrap(True)

        # Add the label to the layout
        layout.addWidget(self.resultLabel)

        # Set the layout for the widget
        self.setLayout(layout)


class UserItemWidget(QWidget):
    # Define a custom signal with user data
    action_triggered = pyqtSignal(str)

    def __init__(self, user_data,numberOfPrediction, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.name_label = QLabel(user_data)
        self.button = QPushButton("Action")
        layout.addWidget(self.name_label)
        if(numberOfPrediction>0):
            layout.addWidget(self.button)
        self.setLayout(layout)

        # Connect the button's clicked signal to the slot function
        self.button.clicked.connect(self.on_action_triggered)

        # Store the user data
        self.user_data = user_data

    def on_action_triggered(self):
        # Emit the custom signal with user data when the button is clicked
        self.action_triggered.emit(self.user_data)


class UserInterface(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("User Interface")
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()
        
        self.goBackButton = QPushButton("Logout", self)
        self.goBackButton.setFixedSize(50, 50)
        self.goBackButton.move(300, 10)
        layout.addWidget(self.goBackButton)
            
        self.goBackButton.clicked.connect(self.goBack)
        print("Username is ",username)
        apiEndpoint = "http://localhost:3000/api/patient/myPatient"
        response = requests.post(apiEndpoint, json={'name': username})
        data = response.json()

        apiEndpoint2 = "http://localhost:3000/api/getUser"
        response2 = requests.post(apiEndpoint2, json={'name': username})
        data2 = response2.json()        

        noPrediction = data2["num"]

        
        dataUser = data["isPatient"]
        # dataUser =['rem','gem','sem']
        # Create list widget
        self.user_list = QListWidget()
        for user in dataUser:
            item = QListWidgetItem()
            # widget = UserItemWidget(user)

            widget = UserItemWidget(user["name"],noPrediction)
            item.setSizeHint(widget.sizeHint())
            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, widget)

            # Connect the custom signal to a slot function
            widget.action_triggered.connect(self.on_action_triggered)    
            
        layout.addWidget(self.user_list)

        # Create Add button
        self.add_button = QPushButton("Add")
        layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.add_button.clicked.connect(self.addPatient)

        # Create History button
        self.history_button = QPushButton("History")
        layout.addWidget(self.history_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
        self.history_button.clicked.connect(self.showHistory)

        # Create Payment button
        self.payment_button = QPushButton("Payment")
        layout.addWidget(self.payment_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.payment_button.clicked.connect(self.khaltiPayment)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_action_triggered(self, user_data):
        print("Action button clicked for user:", user_data)
        global patientname
        patientname = user_data      
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(5) 

    def goBack(self):
        print("back to login")
        widget.setCurrentIndex(0) 

    def khaltiPayment(self):
        apiEndpoint = "http://localhost:3000/api/payment/esewa"
        response = requests.post(apiEndpoint, json={'name': username})
        data = response.json()
        print(data['payment_url'])
        url = QUrl("www.google.com")
        QDesktopServices.openUrl(url)
        if 'pidx' in data:
            url = QUrl(data["payment_url"])
            QDesktopServices.openUrl(url)
        else:
            print("heo")


    def addPatient(self):
        addPat=AddPatient()
        widget.addWidget(addPat)
        widget.setCurrentIndex(4)

    def showHistory(self):
        history = History()
        widget.addWidget(history)
        widget.setCurrentIndex(3)

class History(QWidget):
    def __init__(self):
        super().__init__()
 
        self.initUI()

    def initUI(self):
        
        self.goBackButton = QPushButton("GoBack", self)
         # Create a table with 2 columns (patient, result)
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["patient", "result"])

        # Create layout and add the table
        layout = QVBoxLayout(self)
        layout.addWidget(self.goBackButton)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('History Table')
        self.setGeometry(100, 100, 400, 300)

        self.goBackButton.clicked.connect(self.goBack)

        self.goBackButton.setFixedSize(50, 50)

        # Fetch and update table data
        self.updateTableData()
    

    def goBack(self):
        widget.setCurrentIndex(2)            


    def updateTableData(self):
        # Make a request to get data
        apiEndpoint = "http://localhost:3000/api/patient/getHistory"
        response = requests.post(apiEndpoint, json={'user': username})
        data = response.json()
        # print(data)

        # Clear existing rows
        self.table.setRowCount(0)

        # Check if 'history' key exists in the response data
        row=0
        if 'history' in data:
            # Iterate over history entries
            for history_entry in data['history']:
                for res in history_entry['result']:
                    print(res)
                    print(history_entry['patient'])
                
                # # Insert a new row at the end of the table
                    self.table.insertRow(row)

                # # Set items in each cell of the new row
                    self.table.setItem(row, 0, QTableWidgetItem(history_entry['patient']['name']))
                    self.table.setItem(row, 1, QTableWidgetItem(str(res)))
                    row=row+1


class AddPatient(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("addPatient.ui",self)
        self.signupbutton.clicked.connect(self.addedfunction)

        layout = QVBoxLayout()
        
        self.goBackButton = QPushButton("GoBack", self)
        self.goBackButton.setStyleSheet("color: white; border: 2px solid #333333;")
        self.goBackButton.setFixedSize(80, 50)
        self.goBackButton.move(20, 10)
        layout.addWidget(self.goBackButton)
            
        self.goBackButton.clicked.connect(self.goBack)

    def goBack(self):
        widget.setCurrentIndex(2)  

    def addedfunction(self):
        name=self.name.text()
        age = int (self.age.text())
        gender = self.gender.text()
        data = {
            'name': name,
            'age': age,
            'gender':gender,
            'user':username
                }
        headers = {
   
        'Content-Type': 'application/json',

            }
        apiEndpoint = "http://localhost:3000/api/patient/add"
        response = requests.post(apiEndpoint, json=data, headers=headers)

        print(response)


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
    def loginfunction(self):
        name = self.name.text()
        password = self.password.text()            
        data = {
            'name': name,
            'password': password,
                }
        headers = {
        'Content-Type': 'application/json',

            }
        apiEndpoint = "http://localhost:3000/api/login"
        response = requests.post(apiEndpoint, json=data, headers=headers)
        res = json.dumps(response.json())
        res = json.loads(res)
        s = res["success"]
        m = res["msg"]
        id = s
        if(s==False):
            print(m)
        else:
            global username
            
            username = name
            
            print("Successfully logged in with name: ", name, "and password:", password)
            UserPage=UserInterface()
            widget.addWidget(UserPage)
            widget.setCurrentIndex(2)


    def gotocreate(self):
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(1)
        print(widget.currentIndex())



class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("userPage.ui",self)
        layout = QVBoxLayout()
        
        self.goBackButton = QPushButton("GoBack", self)
        self.goBackButton.setStyleSheet("color: white; border: 2px solid #333333;")
        self.goBackButton.setFixedSize(80, 50)
        self.goBackButton.move(20, 10)
        layout.addWidget(self.goBackButton)
            
        self.goBackButton.clicked.connect(self.goBack)

         
        self.signupbutton.clicked.connect(self.createAccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def goBack(self):
        widget.setCurrentIndex(0)         
        print(widget.currentIndex())
    def createAccfunction(self):
        name = self.name.text()
        password = self.password.text()  
        confirmPassword=self.confirmpass.text()
        print("Button Post clicked")
        data = {
            'name': name,
            'password': password,
                }
        headers = {
   
        'Content-Type': 'application/json',

            }


        apiEndpoint = "http://localhost:3000/api/register"
        response = requests.post(apiEndpoint, json=data, headers=headers)
        res = response.json()


        if password==confirmPassword:
            if(res["success"]==False):
                print("Cannot create an account cause "+ res["msg"])
            else:
                print("Successfully created acc with name: ", name, "and password: ", password)
                login=Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()-1)
                print(widget.currentIndex())

        else:
            print("Your confirm password and password is not same")        

      






app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setCurrentIndex(0)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit
# from PyQt5.QtCore import QObject, pyqtSignal

# class Communicate(QObject):
#     data_updated = pyqtSignal(str)





# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Toggle Classes Example")
#         self.setGeometry(100, 100, 400, 300)

#         self.communicate = Communicate()

#         self.stacked_widget = QStackedWidget()
#         self.setCentralWidget(self.stacked_widget)

#         self.class_a_widget = ClassAWidget(self.communicate,self.stacked_widget)


#         self.stacked_widget.addWidget(self.class_a_widget)

#         self.current_index = 0



#         layout = QVBoxLayout()
#         layout.addWidget(self.stacked_widget)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)



# class ClassAWidget(QWidget):
#     def __init__(self, communicate,stacked_widget):
#         super().__init__()
#         self.label = QLabel("Class A Widget - Value: None")
#         layout = QVBoxLayout()
#         butt = QPushButton("B")
#         layout.addWidget(self.label)
#         layout.addWidget(butt)
#         self.setLayout(layout)
#         self.communicate =communicate
#         communicate.data_updated.connect(self.update_label)
#         butt.clicked.connect(self.navigateTo)
#         self.stacked_widget = stacked_widget
#         print("Current Index" + str (self.stacked_widget.currentIndex()))

#     def navigateTo(self):
#         classB = ClassBWidget(self.communicate,self.stacked_widget)
#         self.stacked_widget.addWidget(classB)
#         self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()+1)
#         print("A", self.stacked_widget.currentIndex())

#     def update_label(self, gg):
#         self.label.setText("Class A Widget - Value: " + gg)

# class ClassBWidget(QWidget):
#     def __init__(self, communicate,stacked_widget):
#         super().__init__()
#         layout = QVBoxLayout()

#         self.label = QLabel("Class B Widget - Value: None")
#         butt = QPushButton("A")
#         self.text_field = QLineEdit()
#         self.submit = QPushButton("Submit")
#         self.submit.clicked.connect(self.submitF)        

#         self.stacked_widget = stacked_widget

#         layout.addWidget(self.text_field)
#         layout.addWidget(butt)
#         layout.addWidget(self.label)
#         layout.addWidget(self.submit)

#         self.setLayout(layout)

#         self.communicate = communicate

#         self.communicate.data_updated.connect(self.updateLabel)

#         butt.clicked.connect(self.navigateTo)

#     def submitF(self):
#         text = self.text_field.text()
#         self.communicate.data_updated.emit(text)

        
#     def navigateTo(self):
#         classA = ClassBWidget(self.communicate,self.stacked_widget)
#         self.stacked_widget.addWidget(classA)
#         self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()-1)
#         print("B", self.stacked_widget.currentIndex())

#     def updateLabel(self,val):
#         self.label.setText('Class B Widget - Value: '+val)


# class ClassCWidget(QWidget):
#     def __init__(self,communicate,stacked_widget):
#         super.__init__()
#         self.label = QLabel("Class CCC Widget - Value: None")
#         layout = QVBoxLayout()
#         butt = QPushButton("B")
#         layout.addWidget(self.label)
#         layout.addWidget(butt)
#         self.setLayout(layout)
#         self.communicate =communicate
#         communicate.data_updated.connect(self.update_label)
#         butt.clicked.connect(self.navigateTo)
#         self.stacked_widget = stacked_widget
#         print("Current Index" + str (self.stacked_widget.currentIndex()))

#     def navigateTo(self):
#         classB = ClassBWidget(self.communicate,self.stacked_widget)
#         self.stacked_widget.addWidget(classB)
#         self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()+1)
#         print("A", self.stacked_widget.currentIndex())

#     def update_label(self, gg):
#         self.label.setText("Class A Widget - Value: " + gg)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


