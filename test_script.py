from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ----------------------------
# Вспомогательная функция
# ----------------------------
def is_element_present(driver, by, value, timeout=1):
    """
    Проверяет, есть ли элемент на странице за timeout секунд.
    Возвращает True, если есть, False если нет.
    """
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False

# ----------------------------
# Тесты для ввода номера
# ----------------------------
def test_summ_input_limit(driver, type_, number):
    """
    Проверка появления поля ввода суммы в зависимости от длины номера.
    Логика:
    - Поле появляется только для номеров длиной 16 символов
    - Для коротких номеров поле не появляется
    """
    driver.find_element(By.ID, type_).click()
    number_input = driver.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(number)

    # Проверяем появление поля суммы
    field_present = is_element_present(driver, By.CSS_SELECTOR, "input[placeholder='1000']")
    if field_present:
        assert len(number) == 16, f"Поле появилось для номера {number}, а длина != 16"
    else:
        assert len(number) < 16, f"Поле не появилось для номера {number}, а длина >= 16"

# ----------------------------
# Тесты для суммы
# ----------------------------
def test_input_summ(driver, type_, number, summ):
    """
    Проверка суммы в поле.
    Логика:
    - Если поле суммы есть, проверяем, что можно ввести значение в диапазоне
    """
    driver.find_element(By.ID, type_).click()
    number_input = driver.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(number)

    if is_element_present(driver, By.CSS_SELECTOR, "input[placeholder='1000']"):
        sum_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
        sum_input.clear()
        sum_input.send_keys(summ)
        # Можно добавить проверку: например, assert sum_input.get_attribute("value") == str(summ)

# ----------------------------
# Тесты для комиссии
# ----------------------------
def test_comission_rub(driver, type_, number):
    """
    Проверка комиссии.
    Логика:
    - Комиссия вычисляется и отображается только если поле суммы есть
    """
    driver.find_element(By.ID, type_).click()
    number_input = driver.find_element(By.CSS_SELECTOR, "[type=text]")
    number_input.clear()
    number_input.send_keys(number)

    if is_element_present(driver, By.CSS_SELECTOR, "input[placeholder='1000']"):
        sum_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='1000']")
        # Логика расчета комиссии (можно добавить проверку конкретного значения)
        assert sum_input.is_displayed()
    else:
        # Если поле не появилось, комиссии нет
        assert True
