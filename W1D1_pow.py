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
    startTime = time.time()
    _4EndTime = 0
    _5EndTime = 0
    _4nonce = 0
    nonce = 1 
    while(True):
        
        name = "rayer"
        temp = name + str(nonce)
        secreted = hashlib.sha256(temp.encode()).hexdigest()
        print("当前密文为:", secreted)
        if(secreted[0:4] == "0000"):
            _4EndTime = time.time()
            _4nonce = nonce
            if(secreted[0:5] == "00000"):
                _5EndTime = time.time()
                break
        nonce += 1

    print("找到4位为0的nonce时间为：", _4EndTime-startTime, "秒")
    print("找到5位为0的nonce时间为：", _5EndTime-startTime, "秒")
    print("签名：", rsa_private_sign(name+str(_4nonce)))
    print("公钥：", public_key)
    print("用户名：", name, "nonce:", _4nonce)