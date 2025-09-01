# test_script.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# фикстура для драйвера
@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")  # запускаем без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")
    yield driver
    driver.quit()


# сохраняем твои функции без изменений
def test_input_number_rub(driver, type="rub-sum", number="2222222222222222"):
    click_block = driver.find_element(By.ID, type)
    click_block.click()
    number_input = driver.find_element(By.CSS_SELECTOR, "[type = text]")
    number_input.clear()
    number_input.send_keys(number)


def test_input_summ_rub(driver, type="rub-sum", num="10000"):
    test_input_number_rub(driver, type, "2222222222222222")
    summ = driver.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
    summ.clear()
    summ.send_keys(num)
    summ.clear()


def test_comission(driver, type="rub-sum", summa=10000):
    test_input_summ_rub(driver, type, summa)
    comission = driver.find_element(By.ID, "comission")
    try:
        if int(comission.text) == int(summa) * 0.1:
            print("hi")
        else:
            print("ошибка")
    except ValueError:
        print("невозможно преобразовать значение")
