import logging
import dearpygui.dearpygui as dpg
from chat_client import ChatClient
from generic_callback import GenericCallback
import os
from basic_gui import BasicGUI, DEFAULT_VALUES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives import padding, hashes
import base64



DM_SIZE= 16
NB_ITERATIONS= 100000
SIZE_BLOCK = 128
SALT ="data"

class CipheredGUI(BasicGUI):

    def init_(self)->None:
        super()._init()
        self._key = None

    
    def _create_chat_window(self)->None:
        # chat windows
        # known bug : the add_input_text do not display message in a user friendly way
        with dpg.window(label="Chat", pos=(0, 0), width=800, height=600, show=False, tag="chat_windows", on_close=self.on_close):
            dpg.add_input_text(default_value="Readonly\n\n\n\n\n\n\n\nfff", multiline=True, readonly=True, tag="screen", width=790, height=525)
            dpg.add_input_text(default_value="some text", tag="input", on_enter=True, callback=self.text_callback, width=790)


    def _create_connection_window(self)->None: 
        # windows about connexion
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            
            self._log.info("Ajout d'un champ mot de passe")
            #add password field
            dpg.add_text("password")      
            dpg.add_input_text(password=True,tag="connection_password")
            dpg.add_button(label="Connect", callback=self.run_chat)

    def _create_menu(self)->None:
        # menu (file->connect)
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Connect", callback=self.connect)

    def create(self):
        # create the context and all windows
        dpg.create_context()

        self._create_chat_window()
        self._create_connection_window()
        self._create_menu()        
            
        dpg.create_viewport(title='Secure chat - or not', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def update_text_screen(self, new_text:str)->None:
        # from a nex_text, add a line to the dedicated screen text widget
        text_screen = dpg.get_value("screen")
        text_screen = text_screen + "\n" + new_text
        dpg.set_value("screen", text_screen)

    def text_callback(self, sender, app_data)->None:
        # every time a enter is pressed, the message is gattered from the input line
        text = dpg.get_value("input")
        self.update_text_screen(f"Me: {text}")
        self.send(text)
        dpg.set_value("input", "")

    def connect(self, sender, app_data)->None:
        # callback used by the menu to display connection windows
        dpg.show_item("connection_windows")
        

    def run_chat(self, sender, app_data)->None:

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



        #Derivation of the key

    
        kdf= PBKDF2HMAC(algorithm=hashes.SHA256(),length = DM_SIZE,salt=SALT,iterations = NB_ITERATIONS)
        b_password = bytes(password,"utf8")
        self._key = kdf.derive(b_password)
        self._log.info(f"self.key {self._key}")
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")


    def encrypt(self, message):

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv),backend=default_backend()) 
        encryptor = cipher.encryptor()
    
        
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return (iv,ciphertext)


    def decrypt(self, message: bytes):
        msg = base64.b64decode(message[1]['data'])
        iv = base64.b64decode(message[0]['data'])
        cipher = Cipher( algorithms.AES(self._key), modes.CTR(iv),backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(msg) + decryptor.finalize()
        unpadder = padding.PKCS7(SIZE_BLOCK).unpadder()
        unpadded = unpadder.update(decrypted) + unpadder.finalize()
        return unpadded.decode("utf-8")

    def recv(self) -> None:
        # function called to get incoming msgs and display them
        if self._callback is not None:
            for msg in self._callback.get():
                user, msg = msg
                decrypted_msg = self.decrypt(msg)
                self.update_text_screen(f"{user} : {decrypted_msg}")
            self._callback.clear()
        


    def send(self, text):
        # function called to send a message to all (broadcasting)
        encrypted_message = self.encrypt(text)
        self._client.send_message(encrypted_message)

    def loop(self):
        # main loop
        while dpg.is_dearpygui_running():
            self.recv()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()
   


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()
    