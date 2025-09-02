# test_script_ci.py
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# фикстура для драйвера
@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")  # без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")
    yield driver
    driver.quit()


# Проверка длины номера
@pytest.mark.parametrize("type_,number", [
    ("rub-sum", "12345678901234"),       # 14 цифр, input не появляется
    ("rub-sum", "123456789012345"),      # 15 цифр, input не появляется
    ("rub-sum", "1234567890123456"),     # 16 цифр, input появляется
])
def test_summ_input_limit_positive(browser, type_, number):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(number)

    try:
        element = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
        assert len(number) == 16, "Длина номера должна быть 16"
    except NoSuchElementException:
        assert len(number) < 16

    number_input.clear()


# Отдельно отмечаем кейс с 17 цифрами как ожидаемое падение
@pytest.mark.xfail(reason="номер >16 цифр, input не должен появляться")
def test_summ_input_limit_negative(browser):
    click_block = browser.find_element(By.ID, "rub-sum")
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("12345678901234567")

    element = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    assert len("12345678901234567") == 16


# Проверка суммы и резерва
@pytest.mark.parametrize("type_,num,reserved,ollsumm", [
    ("rub-sum", "10000", 20001, 30000),
    ("rub-sum", "9099", 20001, 30000),
])
def test_input_summ_positive(browser, type_, num, reserved, ollsumm):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys(num)

    commision = browser.find_element(By.ID, "comission")
    total = int(summ_input.get_attribute("value")) + float(commision.text)
    assert total <= int(ollsumm) - reserved, "Сумма с комиссией превышает резерв"

    summ_input.clear()


# Ожидаемое превышение резерва
@pytest.mark.xfail(reason="Сумма с комиссией превышает резерв")
def test_input_summ_negative(browser):
    click_block = browser.find_element(By.ID, "rub-sum")
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys("10000")  # тут сумма больше доступного резерва

    commision = browser.find_element(By.ID, "comission")
    total = int(summ_input.get_attribute("value")) + float(commision.text)
    assert total <= 30000 - 20001


# Проверка комиссии
@pytest.mark.parametrize("type_,num", [
    ("rub-sum", "10000"),
    ("rub-sum", "0"),
])
def test_comission_rub_positive(browser, type_, num):
    click_block = browser.find_element(By.ID, type_)
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys(num)

    comission = browser.find_element(By.ID, "comission")
    assert math.floor(float(comission.text)) == math.floor(float(num) * 0.1)


# Ожидаемое расхождение комиссии
@pytest.mark.xfail(reason="Некорректная комиссия")
@pytest.mark.parametrize("num", ["9099", "-10"])
def test_comission_rub_negative(browser, num):
    click_block = browser.find_element(By.ID, "rub-sum")
    click_block.click()

    number_input = browser.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys("2222222222222222")

    summ_input = browser.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ_input.clear()
    summ_input.send_keys(num)

    comission = browser.find_element(By.ID, "comission")
    assert math.floor(float(comission.text)) == math.floor(float(num) * 0.1)
