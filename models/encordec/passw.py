from werkzeug.security import generate_password_hash, check_password_hash

def passGen(passwd):

    return generate_password_hash(passwd)




def passCheck(passgen ,passwd):

    return check_password_hash(passgen, passwd)