import random as random
from constants import * 

#---------------FUNCTIONS TO GENERATE INPUTS WITH FUZZ--------------------#

def get_one_random_domain(domains):
    return random.choice(domains)

def get_one_random_name(letters):
    return ''.join(random.choice(letters) for i in range(7))

def generate_random_email():
    return (get_one_random_name(mix_letters) + '@' + get_one_random_domain(domains))

def generate_text(max_len = 100):
    return(''.join(random.choice((letters_numbers)) for i in range(max_len)))

def generate_num_str(max_len = 100):
    return(''.join(str(random.choice(numbers)) for i in range(max_len)))

def generate_float(max_len = 100):
    #generates float or int
    num_str = generate_num_str()
    num_str+= '.' + generate_num_str(5)
    return(float(num_str))

def generate_int(max_len = 100):
    val = random.random()
    print(val)
    if(val<=0.5):
        print("Good Integer!")
        num_str = generate_num_str(1) #good int
        print(num_str)
    else:
        print("Bad Integer!")
        num_str = generate_num_str(max_len) #bad int
        print(num_str)
    return(int(num_str))

def generate_good_int():
    print("Good Integer!")
    num_str = generate_num_str(1) #good int
    return(int(num_str))

formvals = [[generate_random_email(), generate_text(), str(generate_int()), str(generate_int()), generate_text(), str(generate_int()), str(generate_int()), str(generate_int()), str(generate_int()), str(generate_int()), generate_text()] if (i%2 == 0) else [generate_random_email(), generate_text(), str(generate_good_int()), str(generate_good_int()), generate_text(), str(generate_good_int()), str(generate_good_int()), str(generate_good_int()), str(generate_good_int()), str(generate_good_int()), generate_text()] for i in range(number_of_tests)]