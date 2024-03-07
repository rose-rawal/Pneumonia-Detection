import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QListWidgetItem
from PyQt5 import QtWidgets,QtCore

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Interface")
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        # Create list widget
        self.user_list = QListWidget()
        for user in ["User 1", "User 2", "User 3", "User 4", "User 5"]:
            item = QListWidgetItem(user)
            self.user_list.addItem(item)

        layout.addWidget(self.user_list)

        # Create Add button
        self.add_button = QPushButton("Add")
        layout.addWidget(self.add_button, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        # Create History button
        self.history_button = QPushButton("History")
        layout.addWidget(self.history_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        # Create Payment button
        self.payment_button = QPushButton("Payment")
        layout.addWidget(self.payment_button, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec_())
