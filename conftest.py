import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")  # режим без окна, работает на GitHub
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

    @pytest.fixture(scope="module" , autouse=True)
    def serve_site():
        import subprocess
        import time
        import os

        process = subprocess.Popen(
            ["python3", "-m" , "http.server" , "8000"],
            cwd= os.path.join(os.path.dirname(__file__), ".." , 'dist') , 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        time.sleep(2)
        yield
        process.terminate()
        process.wait()

        
