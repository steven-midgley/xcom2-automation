from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt

def display_feedback(feedback):
    app = QApplication([])
    label = QLabel(feedback)
    label.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    label.setAttribute(Qt.WA_TranslucentBackground)
    label.setStyleSheet("color: gold; font-size: 20px;")
    label.show()
    app.exec_()