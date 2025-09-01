# test_script.py
import time
import math
from selenium.webdriver.common.by import By

def test_input_number_rub(browser, block_id, number):
    browser.find_element(By.ID, block_id).click()
    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(str(number))


def test_input_summ_rub(browser, block_id, num):
    test_input_number_rub(browser, block_id, "2222222222222222")
    summ = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ.clear()
    summ.send_keys(str(num))


def test_comission(browser, block_id, summa):
    summa = int(summa)
    test_input_summ_rub(browser, block_id, summa)
    comission = browser.find_element(By.ID, "comission")
    commission_value = int(comission.text)
    
    expected = math.floor(summa * 0.1)
    if commission_value == expected:
        print(f"{block_id} {summa}: hi")
    else:
        print(f"{block_id} {summa}: ошибка! ожидалось {expected}, получили {commission_value}")


def test_all_comissions(browser):
    for currency in ["rub-sum", "usd-sum", "euro-sum"]:
        for value in [10000, 9099, -10, 0]:
            test_comission(browser, currency, value)
