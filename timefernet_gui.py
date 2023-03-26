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
        encr= Fernet(self.key)
        new_message= bytes(message,'utf-8')
        temps = int(time.time())
        #Temps = int(time.time())-45
        encryp = encr.encrypt_at_time(new_message,current_time= temps)
        return encryp

    def decrypt(self, message) -> str :
        msg = base64.b64decode(message['data']) 
        decrypted= Fernet(self._key) 
        temps = time.time() 
        temps = int (temps)
        try:
            decrypted_message = decrypted.decrypt_at_time(msg, TTL, temps).decode('utf8') 
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