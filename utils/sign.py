from pathlib import Path
import os

class sign(object):
    def __init__(self, ruta_apk):
        self.ruta_apk = ruta_apk
        
    def uberApkSigner(self):
        uberapksigner = Path('resources/tools/uber-apk-signer/uber-apk-signer.jar')
        archivo3 = self.ruta_apk
        exists_file = os.path.isfile(archivo3) # si existe el archivo is true
        extension = os.path.splitext(archivo3)[1]
        if exists_file and extension == '.apk':
            carp_desc = archivo3.replace('.apk','') #ruta carpeta archivo           
            cmd = 'java -jar ' + uberapksigner.as_posix() + ' -a ' + archivo3 + ' -o ' + carp_desc
            return cmd
        else:
            return 'ocurrio un error revise la aplicacion'