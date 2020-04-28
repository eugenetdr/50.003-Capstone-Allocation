from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import time
import random as random
from constants import *

def click_input_by_type_value(driver, input_type, value):
    button = driver.find_elements_by_xpath("//input[@" + input_type + "='" + value + "']")[0]
    button.click()
    time.sleep(2)

def start_driver():
    driver = webdriver.Chrome("/usr/bin/chromedriver")
    driver.get("http://127.0.0.1:8000/")
    return driver

def student_login():
    driver = start_driver()

    log_string = "About to Login.\n"
    time.sleep(2)

    click_input_by_type_value(driver, "value", "Student")

    student_user= driver.find_elements_by_xpath("//input[@placeholder='Username']")[0]
    student_password = driver.find_elements_by_xpath("//input[@placeholder='Password']")[0]

    student_user.send_keys(usernames[0])
    student_password.send_keys(passwords[0])

    click_input_by_type_value(driver, "value", "Login")

    review_request_start(driver, log_string, 0)

def review_request_start(driver, log_string, recurse_count = 0): #either edit or logout
    if(recurse_count>3):
        logout(log_string)
    else:
        val = random.random()
        print(val)
        if(val<=0.7):
            edit_request(driver, log_string, recurse_count+1)
        else:
            logout(driver, log_string)


def edit_request(driver, log_string, recurse_count):
    val = random.random()
    print(val)
    if(val<=0.7):
        log_string += "Inputing Edit Form Values.\n"
        click_input_by_type_value(driver, "value", "Edit Request")

        powerpoints = driver.find_elements_by_xpath("//input[@name='powerpoints']")[0]

        #submit = get_input_by_type_value("value", "Submit Space Request") #driver.find_elements_by_xpath("//input[@value='Submit Space Request']")[0]

        values = formvals[0]

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
        
        click_input_by_type_value(driver, "value", "Submit Space Request")
        review_after_edit(driver, log_string, recurse_count)
    else:
        logout(driver, log_string)


def review_after_edit(driver, log_string, recurse_count):
    log_string += "Reviewing Entered Request.\n"
    click_input_by_type_value(driver, "value", "Review Space Request")
    review_request_start(driver, log_string, recurse_count)


def logout(driver, log_string):
    log_string += "Logged out.\n"
    click_input_by_type_value(driver, "value", "Logout")
    #logout_button = driver.find_elements_by_xpath("//input[@value='Logout']")[0]
    #logout_button.click()
    print(log_string)
