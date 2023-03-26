import logging
import hashlib
import base64
import dearpygui.dearpygui as dpg
from generic_callback import GenericCallback
from chat_client import ChatClient
from ciphered_gui import BasicGUI, DEFAULT_VALUES, CipheredGUI
from cryptography.fernet import Fernet

class FernetGUI(CipheredGUI):


    def run_chat(self, sender, app_data)-> None:
        # callback uskeyed by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

      
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")
         # generating key
        self.key = hashlib.sha256(password.encode()).digest()
        self.key = base64.b64encode(self.key)


    def encrypt(self, message):
        '''
        chiffre le message avec Fernet
        '''
        cipher_suite = Fernet(self.key)
        message_bytes = bytes(message,'utf-8')
        cipher_text = cipher_suite.encrypt(message_bytes)
        return cipher_text

    def decrypt(self, message) -> str :
        message = base64.b64decode(message['data']) 
        decrypted = Fernet(self._key)
        decrypted_message = decrypted.decrypt(message).decode('utf8') 
        
        self._log.info(f"Message déchiffré : {decrypted_message}") 

        return decrypted_message 
    
    
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()