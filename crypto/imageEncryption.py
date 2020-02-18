from Crypto.Cipher import AES
from cryptoParams import CryptoParams
from PIL import Image
import binascii
import math

cp = CryptoParams()
cp.generateParamsChaos()
iv = cp.getIvRandom()
key = cp.getKeyChaos()


with open("crypto/kitten.jpg", "rb") as f:
    input_data = f.read()

cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
enc_data = cfb_cipher.encrypt(input_data)

with open("crypto/encryptedKitten.bmp", "wb") as enc_file:
    enc_file.write(enc_data)

im = Image.open("crypto/encryptedKitten.bmp")
im.show()

# with open("crypto/encryptedKitten.jpg", "wb") as enc_file:
#     enc_file.write(enc_data)