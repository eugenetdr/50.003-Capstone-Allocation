from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import time
import string
from generate_inputs import *
from student_route_fns import *

#Testing the Student Side Inputs

driver = webdriver.Chrome("/usr/bin/chromedriver")

driver.get("http://127.0.0.1:8000/")

for j in range(len(usernames)):
    edit = False
    first = False
    
    time.sleep(2)
    admin_button = driver.find_elements_by_xpath("//input[@value='Student']")[0]
    admin_button.click()

    time.sleep(2)

    student_user= driver.find_elements_by_xpath("//input[@placeholder='Username']")[0]
    student_password = driver.find_elements_by_xpath("//input[@placeholder='Password']")[0]
    student_user.send_keys(usernames[j])
    student_password.send_keys(passwords[j])

    login_button = driver.find_elements_by_xpath("//input[@value='Login']")[0]
    login_button.click()

    time.sleep(2)

    try:

        edit = driver.find_elements_by_xpath("//input[@value='Edit Request']")[0]
        edit.click()
        edit = True
        time.sleep(2)

    except:
        first = True
        print("Its the first space request.")

    

    powerpoints = driver.find_elements_by_xpath("//input[@name='powerpoints']")[0]

    

    values = formvals[j]

    for i in range(len(ids)):
        current_input = driver.find_elements_by_xpath("//input[@id='" + ids[i] + "']")[0]
        current_input.clear()
        current_input.send_keys(values[i])

    for radio in radio_ids:
        radio_input = driver.find_elements_by_xpath("//input[@id='" + radio + "']")[0]
        radio_input.click()
    try:
        current_input = driver.find_elements_by_xpath("//input[@id='industry']")[0]
        current_input.clear()
        current_input.send_keys("Architecture")
    except:
        print("No Industry Text field.")
    
    submit = driver.find_elements_by_xpath("//input[@value='Submit Space Request']")[0]
    submit_enabled = submit.get_property('disabled')
    print(submit_enabled)
    if(submit_enabled):
        submit.click()
        time.sleep(2)

        review = driver.find_elements_by_xpath("//input[@value='Review Space Request']")[0]
        review.click()

        time.sleep(2)

        logout_button = driver.find_elements_by_xpath("//input[@value='Logout']")[0]
        logout_button.click()

        time.sleep(3)

        back = driver.find_elements_by_xpath("//input[@value='Back']")[0]
        back.click()

        time.sleep(2)
    else:
        print("Test showed bad inputs!")
        logout_button = driver.find_elements_by_xpath("//input[@value='Logout']")[0]
        logout_button.click()

        time.sleep(3)

        back = driver.find_elements_by_xpath("//input[@value='Back']")[0]
        back.click()

        time.sleep(2)


"""
#Test Admin Side

time.sleep(2)

logout_button = driver.find_elements_by_xpath("//input[@value='Logout']")[0]
logout_button.click()

time.sleep(3)

back = driver.find_elements_by_xpath("//input[@value='Back']")[0]
back.click()

time.sleep(2)

admin = driver.find_elements_by_xpath("//input[@value='Admin']")[0]
admin.click()

time.sleep(2)

admin_user= driver.find_elements_by_xpath("//input[@placeholder='Username']")[0]
admin_password = driver.find_elements_by_xpath("//input[@placeholder='Password']")[0]
admin_user.send_keys("admin")
admin_password.send_keys("admin")

login_button = driver.find_elements_by_xpath("//input[@value='Login']")[0]
login_button.click()

time.sleep(2)

approve = driver.find_elements_by_xpath("//input[@value='Approve']")[0]
approve.click()

time.sleep(2)

approve_all = driver.find_elements_by_xpath("//input[@value='Approve All']")[0]
approve_all.click()

time.sleep(4)

home = driver.find_elements_by_xpath("//button[@type='button']")[0]
home.click()

time.sleep(2)

edit_floorplan = driver.find_elements_by_xpath("//input[@value='Edit Floorplan Level 1']")[0]
edit_floorplan.click()

time.sleep(2)

for obj_id in range(2020001, 2020100):
    str_id = str(obj_id)
    try:
        source_element = driver.find_elements_by_xpath("//div[@id='" + str_id + "']")[0]
        ActionChains(driver).drag_and_drop_by_offset(source_element, 100,100).perform()
        time.sleep(0.01)
    except Exception as e:
        print(e)
        print(str_id)
        continue

save_floorplan = driver.find_elements_by_xpath("//input[@value='Save Allocation']")[0]
save_floorplan.click()

time.sleep(5)

home = driver.find_elements_by_xpath("//input[@value='Home']")[0]
home.click()

time.sleep(2)

view_reqs = driver.find_elements_by_xpath("//input[@value='View Requirements']")[0]
view_reqs.click()

time.sleep(1)

driver.find_element_by_xpath("//select[@name='yearOfGrad']/option[text()='" + str(2020) + "']").click()
submit_year = driver.find_elements_by_xpath("//input[@type='submit']")[0]
submit_year.click()

time.sleep(3)

home = driver.find_elements_by_xpath("//input[@value='Home']")[0]
home.click()

time.sleep(2)

algo = driver.find_elements_by_xpath("//input[@value='runAlgo']")[0]
algo.click()

time.sleep(2)

edit_floorplan = driver.find_elements_by_xpath("//input[@value='Edit Floorplan Level 1']")[0]
edit_floorplan.click()

time.sleep(2)

save_floorplan = driver.find_elements_by_xpath("//input[@value='Save Allocation']")[0]
save_floorplan.click()

time.sleep(2)

home = driver.find_elements_by_xpath("//input[@value='Home']")[0]
home.click()

time.sleep(2)

logout_button = driver.find_elements_by_xpath("//input[@value='Logout']")[0]
logout_button.click()
"""