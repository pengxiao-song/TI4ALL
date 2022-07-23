import multiprocessing
import sys

from PyQt5.QtWidgets import QApplication

from src.app import MainWidget

if  __name__ == "__main__":   
    multiprocessing.freeze_support()
    
    app = QApplication(sys.argv)
    
    main_window = MainWidget()
    main_window.show()

    sys.exit(app.exec_())
