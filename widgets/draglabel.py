from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

class DragLabel(QLabel):
	path = pyqtSignal(str)
	def __init__(self, *args, **kwargs):
		super(DragLabel, self).__init__(*args, **kwargs)
		self.setAcceptDrops(True)	
		
		self.ruta = ""

    # funciones para drag and drop 
	def dragEnterEvent(self, e):
		self.setStyleSheet("QLabel:hover {background-color: White;}")
		if e.mimeData().hasUrls():
			e.accept()
			
		else:
			e.ignore()
	def dropEvent(self, e):
		self.setStyleSheet("QLabel:hover {background-color: White;}")
		if e.mimeData().hasUrls():
			e.accept()
			for url in e.mimeData().urls():
				self.ruta = url.toLocalFile()

			self.path.emit(self.ruta)
			
		else:
			e.ignore()