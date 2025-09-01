from selenium.webdriver.common.by import By

def test_input_number_rub(browser, block_id, num):
    browser.get("http://localhost:8000/index.html")
    elem = browser.find_element(By.ID, block_id)
    elem.clear()
    elem.send_keys(num)
    assert elem.get_attribute("value") == num

def test_input_summ_rub(browser, block_id, summa):
    browser.get("http://localhost:8000/index.html")
    elem = browser.find_element(By.ID, block_id)
    elem.clear()
    elem.send_keys(str(summa))
    assert elem.get_attribute("value") == str(summa)

def test_comission(browser, block_id, summa):
    browser.get("http://localhost:8000/index.html")
    elem = browser.find_element(By.ID, block_id)
    elem.clear()
    elem.send_keys(str(summa))
    # Тут можешь добавить проверку комиссии
    assert elem.get_attribute("value") == str(summa)

def test_all_comissions(browser):
    for currency in ["rub-sum", "usd-sum", "euro-sum"]:
        for value in [10000, 9099, -10, 0]:
            browser.get("http://localhost:8000/index.html")
            elem = browser.find_element(By.ID, currency)
            elem.clear()
            elem.send_keys(str(value))
            assert elem.get_attribute("value") == str(value)
