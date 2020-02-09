from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from chopper import Chopper
import sys


class ChopperGUI:
    def __init__(self):
        app = QApplication([])
        app.setStyle("Macintosh")
