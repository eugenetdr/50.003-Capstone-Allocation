from student_route_fns import *

floorplan_lvls = {1: "Edit First Floor", 2: "Edit Second Floor"}

def admin_login():
    driver = start_driver()

    log_string = "About to Login.\n"
    time.sleep(2)

    click_input_by_type_value(driver, "value", "Admin")

    user= driver.find_elements_by_xpath("//input[@placeholder='Username']")[0]
    password = driver.find_elements_by_xpath("//input[@placeholder='Password']")[0]

    user.send_keys("admin")
    password.send_keys("admin")

    click_input_by_type_value(driver, "value", "Login")

    main_page(driver, log_string, 0)

def main_page(driver, log_string, recurse_count):
    val = random.random()
    print(val)
    if(val<=0.2):
        view_requests(driver, log_string, recurse_count)
    elif(val<=0.4):
        approve_requests(driver, log_string, recurse_count)
    elif(val<=0.6):
        edit_floorplan(driver, log_string, recurse_count, 1, True)
    elif(val<=0.8):
        edit_floorplan(driver, log_string, recurse_count, 2, True)
    elif(val<=1.0):
        logout(driver, log_string)

def view_requests(driver, log_string, recurse_count):
    log_string+="Viewing Requests.\n"
    click_input_by_type_value(driver, "value", "View Requirements")
    return_home(driver, log_string, recurse_count)
    
def return_home(driver, log_string, recurse_count):
    log_string+="Returning Home.\n"
    click_input_by_type_value(driver, "value", "Home")
    recurse_count+=1
    if(recurse_count > 10):
        logout(driver, log_string)
    main_page(driver, log_string, recurse_count)

def approve_requests(driver, log_string, recurse_count):
    log_string += "Approving Requests.\n"
    click_input_by_type_value(driver, "value", "Approve")
    val = random.random()
    print(val)
    if(val<=0.5):
        logout(driver, log_string)
    else:
        return_home(driver, log_string, recurse_count)

def edit_floorplan(driver, log_string, recurse_count, level, first):
    log_string += "Editing Level " + str(level) + " Floorplan.\n"
    if(first):
        click_input_by_type_value(driver, "value", "Edit Floorplan Level " + str(level))
    else:
        click_input_by_type_value(driver, "value", floorplan_lvls[level])
    if(recurse_count > 10):
        return_home(driver, log_string, recurse_count)
    val = random.random()
    print(val)
    if(val<=0.5):
        return_home(driver, log_string, recurse_count)
    else:
        if(level == 1):
            edit_floorplan(driver, log_string, recurse_count+1, 2, False)
        else:
            edit_floorplan(driver, log_string, recurse_count+1, 1, False)




