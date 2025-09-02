# test_script_fixed.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math

# -------------------
# Вспомогательная функция: поиск опционального элемента
# -------------------
def find_optional_element(driver, by, selector, timeout=3):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
    except TimeoutException:
        return None

# -------------------
# Тест ограничения длины номера карты
# -------------------
@pytest.mark.parametrize("type_,number", [
    ("rub-sum", "12345678901234"),       
    ("rub-sum", "123456789012345"),      
    ("rub-sum", "1234567890123456"),     
    ("rub-sum", "12345678901234567"),    
])
def test_summ_input_limit(browser, type_, number):
    wait = WebDriverWait(browser, 10)

    click_block = browser.find_element((By.ID, type_))
    click_block.click()

    number_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[type=text]")))
    number_input.clear()
    number_input.send_keys(number)

    # Проверка появления поля суммы
    sum_input = find_optional_element(browser, By.CSS_SELECTOR, "input[placeholder='1000']", timeout=3)
    if sum_input:
        assert len(number) == 16, "больше 16 чисел ошибка"
    else:
        assert len(number) < 16

    number_input.clear()

# -------------------
# Тест ввода суммы
# -------------------
@pytest.mark.parametrize("type_,num,reserved", [
    ("rub-sum", "10000", 20001),
    ("rub-sum", "9099", 20001),
    ("rub-sum", "-10", 20001),
    ("rub-sum", "0", 20001),
])
def test_input_summ(browser, type_, num, reserved):
    wait = WebDriverWait(browser, 10)

    click_block = browser.find_element((By.ID, type_))
    click_block.click()

    number_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[type=text]")))
    number_input.clear()
    number_input.send_keys("2222222222222222")

    # Опциональное поле суммы
    summ_input = find_optional_element(browser, By.CSS_SELECTOR, "input[placeholder='1000']", timeout=3)
    if summ_input:
        summ_input.clear()
        summ_input.send_keys(num)

        commision = find_optional_element(browser, By.ID, "comission", timeout=3)
        oll_sum_text = browser.find_element(By.ID, type_).text

        total = int(summ_input.get_attribute("value")) + float(commision.text)
        assert total <= int(oll_sum_text) - reserved, f"Сумма с комиссией больше чем доступный резерв {reserved}"

        summ_input.clear()

# -------------------
# Тест комиссии конкретно для рубля
# -------------------
@pytest.mark.parametrize("type_,num", [
    ("rub-sum", "10000"),
    ("rub-sum", "9099"),
    ("rub-sum", "-10"),
    ("rub-sum", "0"),
])
def test_comission_rub(browser, type_, num):
    wait = WebDriverWait(browser, 10)

    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[type=text]")))
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = find_optional_element(browser, By.CSS_SELECTOR, "input[placeholder='1000']", timeout=3)
    if summ_input:
        summ_input.clear()
        summ_input.send_keys(num)

        comission = find_optional_element(browser, By.ID, "comission", timeout=3)
        # Проверка комиссии на месте
        assert math.floor(float(comission.text)) == math.floor(10000 * 0.1), "Комиссия не совпадает"
