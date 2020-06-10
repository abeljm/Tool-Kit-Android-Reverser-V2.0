import itertools
import time
from PyQt5.QtCore import pyqtSignal, QThread

class loading(QThread):
    change_value = pyqtSignal(str)
    def __init__(self, parent=None):
        super(loading, self).__init__(parent)
        self.done = True
    def run(self):
        while self.done:
            for c in itertools.cycle(['|', '/', '-', '\\']):
                self.change_value.emit('Espere un momento...    ' + c)
                time.sleep(0.1)      

    def stop(self):
        self.done = False
        self.terminate()