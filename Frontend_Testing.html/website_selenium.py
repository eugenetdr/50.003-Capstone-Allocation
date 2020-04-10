from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

formvals = [["capstone_selenium@capstone.com", "selenium_project", "12", "2", "Required for selenium project", "2", "3", "4", "5", "23", "Automated selenium testing is great."],
["capstone_selenium@fail.com", "Good Luck submitting this form", "fail_value", "null haha", "fail case", "2", "3", "4", "5", "23", "This form should not be submitted"]
]
usernames = ["2020009", "2020005"]
passwords = ["password", "password"]

driver = webdriver.Chrome("/usr/bin/chromedriver")

for j in range(len(formvals)):
    
    driver.get("http://127.0.0.1:8000/")
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

    edit = driver.find_elements_by_xpath("//input[@value='Edit Request']")[0]
    edit.click()

    time.sleep(2)


    ids = ["representativeEmail", "projectName", "bigPedestals", "smallPedestals", "pedestalDescription", "monitors", "TVs", "tables", "chairs", "HDMIAdaptors", "others"]

    radio_ids = ["prototypeType1", "prototypeSize1", "showCaseSize1"]

    powerpoints = driver.find_elements_by_xpath("//input[@name='powerpoints']")[0]

    submit = driver.find_elements_by_xpath("//input[@value='Submit Space Request']")[0]

    values = formvals[j]

    for i in range(len(ids)):
        current_input = driver.find_elements_by_xpath("//input[@id='" + ids[i] + "']")[0]
        current_input.clear()
        current_input.send_keys(values[i])

    for radio in radio_ids:
        radio_input = driver.find_elements_by_xpath("//input[@id='" + radio + "']")[0]
        radio_input.click()

    submit.click()

    time.sleep(2)

    review = driver.find_elements_by_xpath("//input[@value='Review Space Request']")[0]
    review.click()


#keep these separately: prototypeType1, prototypeType2, prototypeType3, prototypeType4, prototypeType5, prototypeCustom
#prototypeSize1, prototypeSize2, prototypeSize3, prototypeSize4, prototypeLength, prototypeWidth, prototypeHeight
#showCaseSize1, showCaseSize1, showCaseSize1, showCaseSize1, showCaseLength, showCaseWidth, showCaseHeight
#Name: powerpoints
#bigPedestals, smallPedestals, pedestalDescription
# use elem.clear()




