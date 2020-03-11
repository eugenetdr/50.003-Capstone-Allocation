import re

def check_email(email):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    result = re.search(regex, email)
    return(result)

def check_general_string(text):
    if((len(text) == 0) or (text == None)):
        return false
    else:
        return true

def check_number(number):
    if(not(isinstance(x, int)) or not(isinstance(x, float))):
        return false
    if(number < 0):
        return false
    return true
    

