
import hashlib
import random
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


def rsa_private_sign(data):
    private_key = get_key('rsa_private_key.pem')
    signer = PKCS1_signature.new(private_key)
    digest = SHA.new()
    digest.update(data.encode("utf8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    signature = signature.decode('utf-8')
    return signature

def decrypt_data(encrypt_msg):
    private_key = get_key('rsa_private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)
    return key

if __name__ == '__main__':

    rsa = RSA.generate(2048)
    # 生成私钥
    private_key = rsa.exportKey()
    print(private_key.decode('utf-8'))
    # 生成公钥
    public_key = rsa.publickey().exportKey()
    print(public_key.decode('utf-8'))
    with open('rsa_private_key.pem', 'wb')as f:
        f.write(private_key)
    
    with open('rsa_public_key.pem', 'wb')as f:
        f.write(public_key)

    name = "rayer"
    
    print("签名：", rsa_private_sign(name + "nonce"))
    print("公钥：", public_key)