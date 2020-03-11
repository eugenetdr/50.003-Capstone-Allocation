
import re

prototype_size_dictionary = {"Small": [1,1,1], "Medium": [1.5,1.5,1.5], "Large": [2,2,2]}
showcase_size_dictionary = {"Small": [1.2,1.2,1.2], "Medium": [1.7,1.7,1.7], "Large":[2.2,2.2,2.2]}

def check_email(email):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    result = re.search(regex, email)
    if(result == None):
        return False
    else:
        return True

def check_general_string(text):
    if((len(text) == 0) or (text == None)):
        return False
    else:
        return True

def check_number(number):
    if(not(isinstance(number, int)) or not(isinstance(number, float))):
        return False
    if(number < 0):
        return False
    return True

def catch_no_input(check_func, request, variable_name):
    try:
        return(check_func(request.POST[variable_name]))
    except MultiValueDictKeyError:
        return(False)
    

