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

def test_remove_from_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    # Kullanıcı adı ve şifre ile giriş yapar.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # İlk ürünü sepete ekler.
    first_product_add_to_cart_button = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn_inventory"))
    )
    first_product_add_to_cart_button.click()

    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link").click

    remove_item = driver.find_element(By.CLASS_NAME, "btn_secondary")
    remove_item.click()

    # Sepetin güncellenip güncellenmediğini kontrol eder.
    cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(cart_badge) == 0  # Eğer sepet boş değilse test başarısız olur.

    cart_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
    )
    cart_icon.click()

    checkout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )
    checkout_button.click()

    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    ).send_keys("John")
