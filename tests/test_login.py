import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = "C:/Program Files (x86)/chromedriver/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "Swag Labs" in driver.title
