from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import math

options = Options()

driver = webdriver.Chrome(options=options)
driver.get("http://localhost:8000/?balance=30000&reserved=20001")

def test_input_number_rub(type , number):
    click_block = driver.find_element(By.ID , type)
    click_block.click()
    number_input = driver.find_element(By.CSS_SELECTOR, "[type = text]")
    number_input.clear()
    number_input.send_keys(number)
'''
test_input_number_rub("rub-sum" , "222222222222222")
test_input_number_rub("usd-sum" , "2222222222222222")
test_input_number_rub("euro-sum" , "22222222222222222")

'''
def test_input_summ_rub(type , num):
    test_input_number_rub(type , "2222222222222222")
    summ = driver.find_element(By.CSS_SELECTOR , "input[placeholder='1000']")
    summ.clear()
    summ.send_keys(num)
    summ.clear()

'''
test_input_summ_rub("rub-sum" , "10000")
test_input_summ_rub("rub-sum","9099")
test_input_summ_rub("rub-sum" ,"-10")
test_input_summ_rub("rub-sum" ,"0")


test_input_summ_rub("usd-sum" , "10000")
test_input_summ_rub("usd-sum","9099")
test_input_summ_rub("usd-sum" ,"-10")
test_input_summ_rub("usd-sum" ,"0")

test_input_summ_rub("euro-sum" , "10000")
test_input_summ_rub("euro-sum","9099")
test_input_summ_rub("euro-sum" ,"-10")
test_input_summ_rub("euro-sum" ,"0")
'''
def test_comission(type ,  summa  ):
    test_input_summ_rub(type , summa)
    comission = driver.find_element(By.ID , "comission")
    if int(comission.text) == summa * 0.1:
        print("hi")
    else:
        print("ошибка")

'''
test_comission("rub-sum" , 10000)
test_comission("rub-sum",9099)
test_comission("rub-sum" ,-10)
test_comission("rub-sum" ,0)


test_comission("usd-sum" , 10000)
test_comission("usd-sum",9099)
test_comission("usd-sum" ,-10)
test_comission("usd-sum" ,0)

test_comission("euro-sum" , 10000)
test_comission("euro-sum",9099)
test_comission("euro-sum" ,-10)
test_comission("euro-sum" ,0)
'''