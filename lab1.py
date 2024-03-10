




import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal
import asyncio

class Communicate(QObject):
    data_updated = pyqtSignal(str)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toggle Classes Example")
        self.setGeometry(100, 100, 400, 300)

        self.communicate = Communicate()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.class_a_widget = ClassAWidget(self.communicate,self.stacked_widget)


        self.stacked_widget.addWidget(self.class_a_widget)

        self.current_index = 0



        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



class ClassAWidget(QWidget):
    def __init__(self, communicate,stacked_widget):
        super().__init__()
        self.label = QLabel("Class A Widget - Value: None")
        layout = QVBoxLayout()
        butt = QPushButton("B")
        layout.addWidget(self.label)
        layout.addWidget(butt)
        self.setLayout(layout)
        self.communicate =communicate
        self.text = None
        communicate.data_updated.connect(self.update_label)

        butt.clicked.connect(self.navigateTo)
        self.stacked_widget = stacked_widget
        print("INside a construtor in Class A",self.text)

    def navigateTo(self):
        classB = ClassBWidget(self.communicate,self.stacked_widget)
        self.stacked_widget.addWidget(classB)
        self.stacked_widget.setCurrentIndex(1)


    def update_label(self, gg):
        self.label.setText("Class A Widget - Value: " + gg)
        self.text =gg
        print("Update in Class A",self.text)

class ClassBWidget(QWidget):
    def __init__(self, communicate,stacked_widget):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Class B Widget - Value: None")
        butt = QPushButton("A")
        butt2 = QPushButton("C")
        self.text_field = QLineEdit()
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.submitF)        
        self.stacked_widget = stacked_widget

        layout.addWidget(self.text_field)
        layout.addWidget(butt)
        layout.addWidget(butt2)
        layout.addWidget(self.label)
        layout.addWidget(self.submit)
        self.passVal= None
        self.setLayout(layout)

        self.communicate = communicate
        self.text = None
        self.communicate.data_updated.connect(self.updateLabel)

        butt.clicked.connect(self.navigateTo)
        butt2.clicked.connect(self.navigateC)


    def submitF(self):
        text = self.text_field.text()
        self.communicate.data_updated.emit(self.text_field.text())
        

        
    def navigateTo(self):
        self.stacked_widget.setCurrentIndex(0)

    def navigateC(self):       

        classC =  ClassCWidget(self.communicate,self.stacked_widget,self.passVal)
        self.stacked_widget.addWidget(classC)
        self.stacked_widget.setCurrentIndex(2)           
        self.communicate.data_updated.emit(self.text_field.text())


    def updateLabel(self,val):
        self.label.setText('Class B Widget - Value: '+val)
        self.passVal = val
        self.text = val
        print("Updated Text in Class B", self.text)

class ClassCWidget(QWidget):
    def __init__(self, communicate, stacked_widget, text):
        super().__init__()
        self.label = QLabel("Class CCC Widget - Value: None")
        layout = QVBoxLayout()
        butt = QPushButton("B")
        layout.addWidget(self.label)
        layout.addWidget(butt)
        self.setLayout(layout)
        butt.clicked.connect(self.navigateTo)
        self.stacked_widget = stacked_widget
        self.communicate = communicate
        self.communicate.data_updated.connect(self.update_label)

        print("In c called a attribute", text)
        print("Current Index" + str(self.stacked_widget.currentIndex()))

    def navigateTo(self):
        self.stacked_widget.setCurrentIndex(1)

    def update_label(self, gg):
        print("Updated in Class C" + gg)
        self.label.setText("Class CCC Widget - Value: " + gg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


