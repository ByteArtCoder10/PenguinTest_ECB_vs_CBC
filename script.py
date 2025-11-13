from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from pathlib import Path
from dotenv import load_dotenv
import base64
import os

load_dotenv() 
key = base64.b64decode(os.getenv("KEY"))
iv = base64.b64decode(os.getenv("IV"))
PATH = Path(os.getenv("IMG_PATH"))
OUTPUT_CBC = Path(os.getenv("OUTPUT_CBC"))
OUTPUT_ECB = Path(os.getenv("OUTPUT_ECB"))
class Test:
    def __init__(self, key, mode, iv=None):
        if mode == AES.MODE_CBC:
            self.cipher = AES.new(key, mode, iv)
        else:
            self.cipher = AES.new(key, mode)
        try:
            with open(PATH, 'rb') as img:
                self.header = img.read(54)
                self.info = img.read()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.info = None
        if mode == AES.MODE_CBC:
            self.encrypt(OUTPUT_CBC)
        else:
                self.encrypt(OUTPUT_ECB)
    
    def encrypt(self, output):
        padded_info = pad(self.info, AES.block_size)
        
        try:     
            encrypted= self.cipher.encrypt(padded_info)
            with open(output, "wb") as img:
                img.write(self.header + encrypted)
            os.startfile(output)
        except Exception as e:
            print(f"Unexpected error: {e}")
def main():
    ecb =Test(key, AES.MODE_ECB)
    cbc =Test(key, AES.MODE_CBC, iv)

if __name__ =="__main__":
    main()

        