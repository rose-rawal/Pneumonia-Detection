


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
import random


from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QHBoxLayout, QLabel, QMainWindow,QVBoxLayout, QPushButton, QDialog, QFileDialog, QListWidget,QListWidgetItem,QTableWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, pyqtSignal, Qt,QObject

from PyQt5.QtGui import QDesktopServices, QFont,QPixmap

class Communicate(QObject):
    patientName = pyqtSignal(str)
    userName = pyqtSignal(str)



class Home(QWidget):
    def __init__(self,communicate):
        super().__init__()
        self.initUI(communicate)

    def initUI(self,communicate):
     
     # Create widgets
     goBackButton = QPushButton('GoBack', self)
     self.patientnamelabel = QLabel("None welcome!!")
     self.patientnamelabel.setStyleSheet("font-weight: bold; color: #FFE8E3; font-size: 28px;background-color:#2A2929; padding-left:10px")
     self.articleLabel = QLabel("..")
     self.articleLabel.setWordWrap(True)    
     self.articleLabel.setStyleSheet("font-weight: bold; color: #A25467; font-size: 20px;background-color:#2A2929; padding:10px")
     self.articleLabel.setFixedHeight(400)
     openFileButton = QPushButton("Open File",self)
     predictButton =QPushButton("Predict", self)
     predictButton.setStyleSheet("color: white;background-color:black;")
     openFileButton.setStyleSheet("color: white; background-color:black;")



     # print("patentname",self.patientName)

     # Connect button click signal to a custom function
     goBackButton.clicked.connect(self.goBack)
     goBackButton.setFixedSize(50, 50)

     openFileButton.clicked.connect(self.upload_image)
     predictButton.clicked.connect(self.predict_result)
     # Create layout and add widgets
     
     layout = QVBoxLayout(self)
     self.username=None
     self.communicate = communicate
     self.communicate.patientName.connect(self.update_patientName)
     self.communicate.userName.connect(self.setUserName)
     self.patientname =None

     layout.addWidget(goBackButton)
     layout.addWidget(self.patientnamelabel)
     layout.addWidget(self.articleLabel)
     layout.addWidget(openFileButton)
     layout.addWidget(predictButton)    
     # Set layout for the main window
     self.setLayout(layout)
     # Set window properties
     self.setWindowTitle('Home Page')
     self.setGeometry(100, 100, 400, 300)

    def update_patientName(self,val):
         articleArr =["Haemophilus influenzae type b (Hib) is a type of bacteria that can cause pneumonia and  meningitis . The Hib vaccine is recommended for all children under 5 years old",
                            "Pneumonia is an infection that inflames your lungs air sacs (alveoli). The air sacs may fill up with fluid or pus, causing symptoms such as a cough, fever, chills and trouble breathing",
                            "Symptoms of pneumonia include cough-(you may cough up yellow or green mucus), fever, shortness of breath, chest pain, fatigue, and in severe cases, confusion."]
         self.patientname = val
         self.patientnamelabel.setText("Welcome!! "+val.upper()) 
         self.articleLabel.setText(random.choice(articleArr))
         print("Home pn ",val)


    def setUserName(self,val):
        self.username = val       
        print("Home un ",val)

    def goBack(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove) 
        widget_to_remove2 = widget.widget(widget.currentIndex()-1)
        widget.removeWidget(widget_to_remove2)
        widget_to_remove3 = widget.widget(widget.currentIndex())
        widget.removeWidget(widget_to_remove3)        
        ui = UserInterface(self.communicate) 
        widget.addWidget(ui)
        widget.setCurrentIndex(1)
        self.communicate.userName.emit(self.username)
        
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

        if 'result' not in globals() or result is None:
            print("An image file was not selected before prediction.") 
        else:   
            predicted_class_index = np.argmax(result)
            class_labels = ['Not Pneumonia', 'Pneumonia'] 
            
            predicted_class_label = class_labels[predicted_class_index]
            print(f'Predicted Class: {predicted_class_label}')
            
            if(predicted_class_label=='Pneumonia'):
                test = True
            else:
                test = False    

            send_data ={
                'user': self.username,
                'result': test,
                'patient':self.patientname,
                
            }
            apiEndpoint = "http://localhost:3000/api/patient/test"
            response = requests.post(apiEndpoint, json=send_data)
            data = response.json()
                
            resWidget = ResultDisplayWidget(self.communicate,predicted_class_label)
            widget_to_remove = widget.widget(widget.currentIndex()+1)
            widget.removeWidget(widget_to_remove) 
            widget.addWidget(resWidget)
            widget.setCurrentIndex(widget.currentIndex()+1)
            self.communicate.patientName.emit(self.patientname)
            self.communicate.userName.emit(self.username)  


        


class ResultDisplayWidget(QWidget): 

    def __init__(self,communicate, text, parent=None):
        super(ResultDisplayWidget, self).__init__(parent)
        self.initUI(communicate,text)

    def initUI(self,communicate,text):
        # Create a vertical layout
        layout = QVBoxLayout()
        self.communicate = communicate
        self.communicate.userName.connect(self.setUsername)
        self.text = text
        self.username = None
        self.communicate.patientName.connect(self.update_label)
        self.resultLabel = QLabel("NOne")
        self.backButt = QPushButton("Back")

        # Set the font for the resultLabel
        self.resultLabel.setStyleSheet("color: black; font-size: 28px;")         
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setFont(QFont("Arial", 16))
        self.resultLabel.setWordWrap(True)
        self.imageLabel = QLabel(widget)

        self.pixmap =QPixmap(None)
        self.imageLabel.setPixmap(self.pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        self.imageLabel.setAlignment(Qt.AlignCenter)     
        # Add the label to the layout
        layout.addWidget(self.resultLabel)
        layout.addWidget(self.imageLabel)

        layout.addWidget(self.backButt)

        # Set the layout for the widget
        self.setLayout(layout)
        self.backButt.clicked.connect(self.backFunc)
    def setUsername(self,val):
        self.username = val
        print("Result Widget ",val)

    def update_label(self,val):
         if(self.text == 'Pneumonia'):
            self.resultLabel.setText(val.upper()+" has "+self.text) 
            self.pixmap =  QPixmap(r"D:\sem7\project\Python\Unhealthy.jpg")
            self.imageLabel.setPixmap(self.pixmap.scaled(300, 300, Qt.KeepAspectRatio))
         else:
            self.resultLabel.setText(val.upper()+" doesn't have Pneumonia") 
            self.pixmap =  QPixmap(r"D:\sem7\project\Python\Healthy.png")
            self.imageLabel.setPixmap(self.pixmap.scaled(300, 300, Qt.KeepAspectRatio))                
         print("ResultDIsplay ",val)   

    def backFunc(self):
        widget_to_remove = widget.widget(widget.currentIndex())
        widget.removeWidget(widget_to_remove) 
        widget_to_remove2 = widget.widget(widget.currentIndex()-1)
        widget.removeWidget(widget_to_remove2)
        widget_to_remove3 = widget.widget(widget.currentIndex())
        widget.removeWidget(widget_to_remove3)        
        ui = UserInterface(self.communicate) 
        widget.addWidget(ui)
        widget.setCurrentIndex(1)
        self.communicate.userName.emit(self.username)
                          

class UserItemWidget(QWidget):
    # Define a custom signal with user data
    # action_triggered = pyqtSignal(str)

    def __init__(self,communicate, user_data,username,numberOfPrediction):
        super().__init__()
        layout = QHBoxLayout()
        self.communicate = communicate
        self.name_label = QLabel(user_data.upper())
        self.button = QPushButton("Action")
        layout.addWidget(self.name_label)
        if(numberOfPrediction>0):
            layout.addWidget(self.button)
        self.setLayout(layout)

        # Connect the button's clicked signal to the slot function
        self.button.clicked.connect(lambda: self.on_action_triggered(user_data,username))

        # Store the user data
        # self.user_data = user_data

    # def on_action_triggered(self):
        # Emit the custom signal with user data when the button is clicked
        # self.action_triggered.emit(self.user_data)
    def on_action_triggered(self, user_data,username):
        
        print("Action button clicked for user:", user_data)
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)               
        home = Home(self.communicate)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)    
        self.communicate.patientName.emit(user_data)
        self.communicate.userName.emit(username)



class UserInterface(QMainWindow):
    def __init__(self,communicate):

        super().__init__()
        self.setWindowTitle("User Interface")
        self.setGeometry(100, 100, 400, 100)

        self.communicate = communicate
        self.username = None
        self.layout = QVBoxLayout()
        
        self.goBackButton = QPushButton("Logout", self)
        self.goBackButton.setFixedSize(50, 50)
        self.goBackButton.move(300, 10)
        self.layout.addWidget(self.goBackButton)
            
        self.goBackButton.clicked.connect(self.goBack)
        self.communicate.userName.connect(self.setUserName)


 
    def setUserName(self, val):
        self.username = val
        print("Username", self.username)
        self.restInit()

    def restInit(self):
        if (self.username =='None'): 
            print("Stfu")
        else:    
            apiEndpoint = "http://localhost:3000/api/patient/myPatient"
            response = requests.post(apiEndpoint, json={'name': self.username})
            data = response.json()

            apiEndpoint2 = "http://localhost:3000/api/getUser"
            response2 = requests.post(apiEndpoint2, json={'name': self.username})
            data2 = response2.json()        


            noPrediction = data2["num"]

            
            dataUser = data["isPatient"]
            
            # dataUser =['rem','gem','sem']
            # Create list widget
            self.user_list = QListWidget()
            for user in dataUser:
                item = QListWidgetItem()
                # widget = UserItemWidget(user)

                widget = UserItemWidget(self.communicate,user["name"],self.username,noPrediction)
                item.setSizeHint(widget.sizeHint())
                self.user_list.addItem(item)
                self.user_list.setItemWidget(item, widget)

                # Connect the custom signal to a slot function
                # widget.action_triggered.connect(self.on_action_triggered)    
                
            self.layout.addWidget(self.user_list)

            # Create Add button
            self.add_button = QPushButton("Add")
            self.layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
            self.add_button.clicked.connect(self.addPatient)

            # Create History button
            self.history_button = QPushButton("History")
            self.layout.addWidget(self.history_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
            self.history_button.clicked.connect(self.showHistory)

            # Create Payment button
            self.payment_button = QPushButton("Payment")
            self.layout.addWidget(self.payment_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
            self.payment_button.clicked.connect(self.khaltiPayment)


            central_widget = QWidget()
            central_widget.setLayout(self.layout)
            self.setCentralWidget(central_widget)        
    def goBack(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)         
        print("back to login")
        widget.setCurrentIndex(0) 

    def khaltiPayment(self):
        apiEndpoint = "http://localhost:3000/api/payment/esewa"
        response = requests.post(apiEndpoint, json={'name': self.username})
        data = response.json()
        print(data['payment_url'])
        url = QUrl("www.google.com")
        QDesktopServices.openUrl(url)
        if 'pidx' in data:
            url = QUrl(data["payment_url"])
            QDesktopServices.openUrl(url)
        else:
            print("Not working khalti")


    def addPatient(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)         
        addPat=AddPatient(self.communicate)
        widget.addWidget(addPat)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.communicate.userName.emit(self.username)  


    def showHistory(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)         
        history = History(self.communicate)
        widget.addWidget(history)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.communicate.userName.emit(self.username)  

        

class History(QWidget):
    def __init__(self, communicate):
        super().__init__()
 
        self.initUI(communicate)

    def initUI(self,communicate):
        self.goBackButton = QPushButton("GoBack", self)
         # Create a table with 2 columns (patient, result)
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["patient", "result","time","date"])

        # Create layout and add the table
        self.username = None
        self.communicate = communicate
        layout = QVBoxLayout(self)
        self.communicate.userName.connect(self.setUserName)
        layout.addWidget(self.goBackButton)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('History Table')
        self.setGeometry(100, 100, 400, 400)

        self.goBackButton.clicked.connect(self.goBack)

        self.goBackButton.setFixedSize(50, 50)

        # Fetch and update table data
        
    
    def setUserName(self,val):
        self.username =val
        print("History ",val)
        self.updateTableData()

    def goBack(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)
        widget_to_remove2 = widget.widget(widget.currentIndex()-1)
        widget.removeWidget(widget_to_remove2)
        widget_to_remove3 = widget.widget(widget.currentIndex())
        widget.removeWidget(widget_to_remove3)        
        ui = UserInterface(self.communicate) 
        widget.addWidget(ui)
        widget.setCurrentIndex(1)
        self.communicate.userName.emit(self.username)
                   


    def updateTableData(self):
        # Make a request to get data
        apiEndpoint = "http://localhost:3000/api/patient/getHistory"
        response = requests.post(apiEndpoint, json={'user': self.username})
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

                # # Insert a new row at the end of the table
                    self.table.insertRow(row)

                # # Set items in each cell of the new row
                    self.table.setItem(row, 0, QTableWidgetItem(history_entry['patient']['name']))
                    self.table.setItem(row, 1, QTableWidgetItem(str(res)))
                    if(history_entry['updatedAt']):
                        self.table.setItem(row, 2, QTableWidgetItem(history_entry['updatedAt'].split('T')[1].split('.')[0]))
                        self.table.setItem(row, 3, QTableWidgetItem(history_entry['updatedAt'].split('T')[0]))

                    else:
                        self.table.setItem(row, 2, QTableWidgetItem('Null'))
                        self.table.setItem(row, 3, QTableWidgetItem('Null'))





                    row=row+1


class AddPatient(QDialog):
    def __init__(self,communicate):
        super().__init__()
        loadUi("addPatient.ui",self)
        self.signupbutton.clicked.connect(self.addedfunction)

        layout = QVBoxLayout()
        self.username = None
        self.communicate = communicate
        self.communicate.userName.connect(self.setUserName)
        self.goBackButton = QPushButton("GoBack", self)
        self.goBackButton.setStyleSheet("color: white; border: 2px solid #333333;")
        self.goBackButton.setFixedSize(80, 50)
        self.goBackButton.move(20, 10)
        layout.addWidget(self.goBackButton)
            
        self.goBackButton.clicked.connect(self.goBack)
    def setUserName(self,val):
        self.username = val
        print("Add Patient ",self.username)
        
    def goBack(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)         
        widget_to_remove2 = widget.widget(widget.currentIndex()-1)
        widget.removeWidget(widget_to_remove2)
        widget_to_remove3 = widget.widget(widget.currentIndex())
        widget.removeWidget(widget_to_remove3)        
        ui = UserInterface(self.communicate) 
        widget.addWidget(ui)
        widget.setCurrentIndex(1)
        self.communicate.userName.emit(self.username)  

    def addedfunction(self):

        if(self.name.text() =="" or self.gender.text()=="" or self.age.text()==""):
            print("While adding the patient enter the required credentials")
        else:    
            name=self.name.text()
            age = int (self.age.text())
            gender = self.gender.text()

            data = {
                'name': name,
                'age': age,
                'gender':gender,
                'user':self.username
                    }
            headers = {

            'Content-Type': 'application/json',

                }
            apiEndpoint = "http://localhost:3000/api/patient/add"
            response = requests.post(apiEndpoint, json=data, headers=headers)

            print("While adding patient ",response)


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.communicate = Communicate()
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
            print("Login Error ",m)

        else:
            print("Successfully logged in with name: ", name, "and password:", password)
            widget_to_remove = widget.widget(widget.currentIndex()+1)
            widget.removeWidget(widget_to_remove)            
            UserPage=UserInterface(self.communicate)
            widget.addWidget(UserPage)
            widget.setCurrentIndex(widget.currentIndex()+1)
            self.communicate.userName.emit(name)  


    def gotocreate(self):
        widget_to_remove = widget.widget(widget.currentIndex()+1)
        widget.removeWidget(widget_to_remove)
    
        createacc=CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        print(widget.currentIndex())



class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("register.ui",self)
        layout = QVBoxLayout()
        
        self.goBackButton = QPushButton("GoBack", self)
        self.goBackButton.setStyleSheet("color: white; border: 2px solid #F4EBF0;")
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
        # print("Button Post clicked")
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
                print("Cannot create an account because you have to "+ res["msg"])
            else:
                print("Successfully created acc with name: ", name, "and password: ", password)
                login=Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()-1)
                print(widget.currentIndex())

        else:
            print("Your confirm password and password is not same")        

      






app=QApplication(sys.argv)



widget=QtWidgets.QStackedWidget()
communicate = Communicate()

mainwindow=Login()

widget.addWidget(mainwindow)

widget.setCurrentIndex(0)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()