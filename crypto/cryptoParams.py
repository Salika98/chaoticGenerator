import secrets
from chaoticGenerator import ChaoticGen
from Crypto.Cipher import AES
from bitstring import BitArray

class CryptoParams(object):
    
    def generateParamsRandom(self):
        key = secrets.token_bytes(AES.block_size)
        iv = secrets.token_bytes(AES.block_size)
        with open("crypto/iv.enc" ,"wb") as f:
            f.write(iv)
        with open("crypto/key.enc" ,"wb") as f:
            f.write(key)
        print(key)
        print(iv)
    
    def generateParamsChaos(self):
        chaos = ChaoticGen(AES.block_size * 8)
        chaosSeq = chaos.mapSequence()
        keyArray = chaosSeq
        keyChaos = ''.join(format(x, 'b') for x in keyArray)
        keyBytes = BitArray(bin = keyChaos).bytes
        print(keyBytes)
        with open("crypto/keyChaos.enc" ,"wb") as f:
            f.write(keyBytes)       


    def getKeyChaos(self):
        with open("crypto/keyChaos.enc" ,"rb") as f:
            key = f.read()
        return key

    def getIvRandom(self):
        with open("crypto/iv.enc" ,"rb") as f:
            iv = f.read()
        return iv

    def getKeyRandom(self):
        with open("crypto/key.enc" ,"rb") as f:
            key = f.read()
        return key

