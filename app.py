# app.py

import sys
from PyQt5.QtWidgets import QApplication
from gui.IntroWindow import IntroWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IntroWindow()
    sys.exit(app.exec_())


