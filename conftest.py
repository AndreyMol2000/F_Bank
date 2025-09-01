# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import time
import os

@pytest.fixture(scope="module")
def serve_site():
    """Поднимаем HTTP сервер на 8000 из папки dist"""
    process = subprocess.Popen(
        ["python3", "-m", "http.server", "8000"],
        cwd=os.path.join(os.path.dirname(__file__), "..", "dist"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # ждём пока сервер стартанёт
    yield
    process.terminate()
    process.wait()


@pytest.fixture(scope="module")
def browser(serve_site):
    """Запускаем Chrome в headless режиме"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
