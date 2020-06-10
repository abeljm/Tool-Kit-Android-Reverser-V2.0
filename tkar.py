import sys
import os
from PyQt5.QtCore import QProcess
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5 import uic
from functools import partial
from utils.resource_path import *
from utils.ProcessOutputReader import *
from utils.descompiler import *
from utils.loading import *
from utils.compiler import *
from utils.sign import *

class tkar(QDialog):
    def __init__(self):
        super(tkar, self).__init__()
        main = resource_path('interface/main.ui')
        uic.loadUi(main, self)
        self.output_process = ''
        self.tabWidget.setStyleSheet("QTabBar::tab { width: 150px; height: 50px; }");
        self.label.path.connect(self.descompile_path)
        self.label_2.path.connect(self.compile_path)
        self.label_3.path.connect(self.sign_path)
        self.btn_smali.clicked.connect(partial(self.descompileApk, "smali"))
        self.btn_java.clicked.connect(partial(self.descompileApk, "java"))
        self.btn_compile.clicked.connect(self.compileApk)
        self.btn_compile_sign.clicked.connect(self.compileAndSignApkOne)
        self.btn_sign.clicked.connect(self.signApk)

    @pyqtSlot(str)
    def descompile_path(self, path):
        self.lineEdit.setText(path)
        self.path = path

    @pyqtSlot(str)
    def compile_path(self, path):
        self.lineEdit_2.setText(path)
        self.path = path

    @pyqtSlot(str)
    def sign_path(self, path):
        self.lineEdit_3.setText(path)
        self.path = path

    @pyqtSlot(str)
    def printLoadingDescompile(self, msj):
        self.label.setText(msj)

    @pyqtSlot(str)
    def printLoadingCompile(self, msj):
        self.label_2.setText(msj)

    @pyqtSlot(str)
    def printLoadingSign(self, msj):
        self.label_3.setText(msj)

    def processTool(self, path, cmd, label, end_process):        
        self.output_process = ''
        self.process = ProcessOutputReader()
        #self.process.produce_output.connect(self.append_output)
        self.path_folder = os.path.abspath(os.path.dirname(path))
        self.log = 'log.txt'
        self.path_log = os.path.join(self.path_folder, self.log)
        self.process.setStandardOutputFile(self.path_log)
        self.process.start(cmd)
        self.process.finished.connect(partial(end_process, label))

    def progressApk(self, func):
        self.thread = loading()
        self.thread.change_value.connect(func)
        self.thread.start()

    def endProcess(self, label):
        self.thread.stop()
        QMessageBox.information(self, "Tool Kit Android Reversing V2.0", "Listo Proceso Culminado, no olvide revisar el log :)", QMessageBox.Ok)
        label.setText("Arrastra la aplicacion...")   

    def descompileApk(self, format):
        if format == 'smali':
            cmd = descompiler(self.path).apktool()
            self.processTool(self.path, cmd, self.label, self.endProcess)                       
            self.progressApk(self.printLoadingDescompile)
        else:
            cmd = descompiler(self.path).jadx()
            self.processTool(self.path, cmd, self.label, self.endProcess)
            self.progressApk(self.printLoadingDescompile)

    def compileApk(self):
        cmd = compiler(self.path).apktool()
        self.processTool(self.path, cmd, self.label_2, self.endProcess)
        self.progressApk(self.printLoadingCompile)

    def compileAndSignApkOne(self):
        comp = compiler(self.path)
        cmd = comp.apktool()
        self.path_two = comp.newApk()
        self.processTool(self.path, cmd, self.label_2, self.compileAndSignApkTwo)
        self.progressApk(self.printLoadingCompile)

    def compileAndSignApkTwo(self,label):
        exists_file = os.path.isfile(self.path_two)  # si existe el archivo is true
        extension = os.path.splitext(self.path_two)[1]
        if exists_file and extension == '.apk':
            self.old_name = self.path_two
            self.new_name = self.path_two.replace('[compiled]', '[CompiledAndSign]')
            os.rename(self.old_name, self.new_name)                   
            cmd = sign(self.new_name).uberApkSigner()
            self.processTool(self.path_two, cmd, label, self.compileAndSignApkThree)

    def compileAndSignApkThree(self, label):
        os.remove(self.new_name)
        self.endProcess(label)

    def signApk(self):
        cmd = sign(self.path).uberApkSigner()
        self.processTool(self.path, cmd, self.label_3)
        self.progressApk(self.printLoadingSign)      

if __name__ == '__main__':
    # Instancia para iniciar una aplicacion
    app = QApplication(sys.argv)
    # Crear un objeto de la clase
    _window = tkar()
    # Muestra la ventana
    _window.show()
    # Ejecutar la aplicacion
    app.exec_()
