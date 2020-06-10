from pathlib import Path
import os

class descompiler(object):
    def __init__(self, ruta_apk):
        self.ruta_apk = ruta_apk

    def jadx(self):
        if os.name == 'nt':
            jadx = Path('resources/tools/jadx/bin/jadx.bat')
        else:
            jadx = Path('resources/tools/jadx/bin/jadx')

        exists_file = os.path.isfile(self.ruta_apk)  # si existe el archivo is true
        extension = os.path.splitext(self.ruta_apk)[1]
        if exists_file and extension == '.apk':
            carp_desc = self.ruta_apk.replace('.apk', '')  # ruta archivo sin extension
            cmd = jadx.as_posix() + ' -d ' + carp_desc + ' ' + self.ruta_apk
            return cmd

    def apktool(self):
        ruta_archivo = self.ruta_apk
        apktool = Path('resources/tools/apktool/apktool.jar')
        exists_file = os.path.isfile(self.ruta_apk)  # si existe el archivo is true
        extension = os.path.splitext(self.ruta_apk)[1]
        if exists_file and extension == '.apk':
            carp_desc = ruta_archivo.replace('.apk', '')  # ruta archivo sin extension
            cmd = 'java -jar ' + apktool.as_posix() + ' d ' + ruta_archivo + ' -o ' + carp_desc
            return cmd