from pathlib import Path
import os

class compiler(object):
    def __init__(self, ruta_apk):
        self.ruta_apk = ruta_apk
        self.new_apk = ''

    def apktool(self):
        ruta_archivo = self.ruta_apk
        apktool = Path('resources/tools/apktool/apktool.jar')
        carp_desc = ruta_archivo.replace('.apk','') #ruta carpeta archivo
        if os.path.isdir(carp_desc):# verificamos si la carpeta existe
            nombre_archivo = os.path.basename(ruta_archivo) # extrae el nombre de la ruta del archivo = archivo.apk
            new_nombre_archivo = '[compiled]' + nombre_archivo # concatena la string new dando como resultado new_archivo.apk
            ruta_archivo2 = ruta_archivo.replace(nombre_archivo, new_nombre_archivo)
            self.new_apk = ruta_archivo2
            cmd = 'java -jar ' + apktool.as_posix() + ' b ' + carp_desc + ' -o ' + ruta_archivo2
            return cmd

    def newApk(self):
        return self.new_apk