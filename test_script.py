# test_script.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import math


@pytest.mark.parametrize("type_,number", [
    ("rub-sum", "12345678901234"),       # 14 цифр, input не появляется
    ("rub-sum", "123456789012345"),      # 15 цифр, input не появляется
    ("rub-sum", "1234567890123456"),     # 16 цифр, input появляется
    ("rub-sum", "12345678901234567"),    # 17 цифр, ошибка
])
def test_summ_input_limit(browser, type_, number):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(number)

    try:
        element = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
        # Если input появился, длина номера должна быть ровно 16
        assert len(number) == 16, "больше 16 чисел ошибка"
    except NoSuchElementException:
        # Если input не появился, длина номера меньше 16
        assert len(number) < 16

    number_input.clear()



@pytest.mark.parametrize("type_,num,reserved", [
    ("rub-sum", "10000", 20001),
    ("rub-sum", "9099", 20001),
    ("rub-sum", "-10", 20001),
    ("rub-sum", "0", 20001),
])
def test_input_summ(browser, type_, num, reserved):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys(num)

    # проверка комиссии
    commision = browser.find_element(By.ID, "comission")
    oll_sum = browser.find_element(By.ID , type_ ).text
    total = int(summ_input.get_attribute("value")) + float(commision.text)
    # логика осталась прежней: сумма с комиссией не должна превышать доступный резерв
    assert total <= int(oll_sum) - reserved, f"Сумма с комиссией больше чем доступный резерв {reserved}"

    summ_input.clear()




@pytest.mark.parametrize("type_,num", [
    ("rub-sum", "10000"),
    ("rub-sum", "9099"),
    ("rub-sum", "-10"),
    ("rub-sum", "0"),
])
def test_comission_rub(browser , type_ , num ):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys(num)

    comission = browser.find_element(By.ID, "comission")
    assert math.floor(float(comission.text)) == math.floor(10000 * 0.1), "Комиссия не совпадает"
