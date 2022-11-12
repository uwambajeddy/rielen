from cryptography.fernet import Fernet

# Put this somewhere safe!
key = 'ivy-cRI3S8sZ1MAlCQpZrsj7X8Nq0Sp1lOnvMbiWdYA='.encode()
f = Fernet(key)

def wordEnc(w):
    token = f.encrypt(str(w).encode())
    return token.decode()

def wordDec(w):

    try:
        p = f.decrypt(str(w).encode())
    except:
        p = -1
    
    if p == -1:
        return -1
    return p.decode()
