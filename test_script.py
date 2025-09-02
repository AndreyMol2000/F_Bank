# test_script.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import math
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


# фикстура для драйвера
@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")  # запускаем без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")
    yield driver
    driver.quit()

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



@pytest.mark.parametrize("type_,num,reserved,ollsumm", [
    ("rub-sum", "10000", 20001  , 30000 ),
    ("rub-sum", "9099", 20001 , 30000),
    ("rub-sum", "-10", 20001 , 30000),
    ("rub-sum", "0", 20001 , 30000),
])
def test_input_summ(browser, type_, num, reserved , ollsumm):
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
    total = int(summ_input.get_attribute("value")) + float(commision.text)
    # логика осталась прежней: сумма с комиссией не должна превышать доступный резерв
    assert total <= int(ollsumm) - reserved, f"Сумма с комиссией больше чем доступный резерв {reserved}"

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
