import string

domains = [ "hotmail.com", "gmail.com", "aol.com", "mail.com" , "mail.kz", "yahoo.com"]
letters = string.ascii_lowercase[:12] 
mix_letters = string.ascii_letters
numbers = [0,1,2,3,4,5,6,7,8,9]
letters_numbers = list(mix_letters) + [str(i) for i in numbers]

ids = ["representativeEmail", "projectName", "bigPedestals", "smallPedestals", "pedestalDescription", "monitors", "TVs", "tables", "chairs", "HDMIAdaptors", "others"]

radio_ids = ["prototypeType1", "prototypeSize1", "showCaseSize1"]

number_of_tests = 20

usernames = ["2020001"]*number_of_tests

passwords = ["F6IxUlad"]*number_of_tests