import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# -------------------
# Фикстура для локального сервера
# -------------------
@pytest.fixture(scope="session", autouse=True)
def serve_site():
    """Запускает HTTP сервер для папки dist/ на localhost:8000"""
    dist_path = os.path.join(os.getcwd(), "dist")
    os.chdir(dist_path)
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    yield
    server.shutdown()
    thread.join()

# -------------------
# Фикстура браузера
# -------------------
@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# -------------------
# Фикстуры для тестовых данных
# -------------------
@pytest.fixture
def block_id():
    # id поля номера карты
    return "rub-sum"

@pytest.fixture
def num():
    return "2222222222222222"

@pytest.fixture
def summa():
    return 10000

# -------------------
# Скриншоты при падении тестов
# -------------------
import pytest
import os

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Делает скриншот при падении теста, если есть фикстура browser"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            file_name = os.path.join(SCREENSHOT_DIR, f"{item.name}.png")
            try:
                browser.save_screenshot(file_name)
                print(f"\nСкриншот при падении сохранён: {file_name}")
            except Exception as e:
                print(f"\nНе удалось сохранить скриншот: {e}")