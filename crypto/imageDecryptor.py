from chaoticGenerator import ChaoticGen
from Crypto.Cipher import AES
from cryptoParams import CryptoParams

cp = CryptoParams()
iv = cp.getIvRandom()
key = cp.getKeyChaos()

with open("crypto/encryptedKitten.enc", "rb") as f:
    enc_data2 = f.read()

cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
plain_data = cfb_decipher.decrypt(enc_data2)

with open("crypto/decryptedKitten.jpg", "wb") as f:
    f.write(plain_data)
