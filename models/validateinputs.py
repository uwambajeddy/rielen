import re
import random

def passwordValidate(passwd):

    #reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
      
    # compiling regex
    #pat = re.compile(reg)
      
    # searching regex                 
    #mat = re.search(pat, passwd)
      
    # validating conditions
    """ if mat:
        return True
    else:
        return False """
    
    if len(passwd) >= 6:
        return True
    else:
        return False
    
    
def EmailValidate(email):

    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):   
        return True 
    else:   
        return False  


def genImageName(filename):
    choices = ['A','a', 'B', 'b','C', 'c', 'D', 'd','E', 'e', 'F', 'f', '1', '2', '3', '4', '5', '9', '10', 'Z', 'z']
    name = filename.split('.')

    nameGen = name[0][:15]
    ext = name[1]

    extName = ''.join(random.choices(choices, k=10))

    return nameGen + extName + '.' + ext