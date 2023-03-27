import logging
import time
import base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from fernet_gui import FernetGUI

TTL = 30


class TimeFernetGUI(FernetGUI):
    def encrypt(self, message):
        '''
        chiffre le message avec Fernet
        '''
        TFERNETENC= Fernet(self.key)
        n_message= bytes(message,'utf-8')
        temps = int(time.time())
        #Temps = int(time.time())-45
        encryp = TFERNETENC.encrypt_at_time(n_message,current_time= temps)
        return encryp

    def decrypt(self, message) -> str :
        msge = base64.b64decode(message['data']) 
        decrypted= Fernet(self._key) 
        temps = time.time() 
        temps = int (temps)
        try:
            decrypted_message = decrypted.decrypt_at_time(msge, TTL, temps).decode('utf8') 
            return decrypted_message 
        except InvalidToken:
            self._log.info("Le message a expiré")
            return "Le message a expiré"
        
    
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()