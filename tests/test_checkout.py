import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = "C:/Program Files (x86)/chromedriver/chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def test_checkout(driver):
    try:
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()
        # Kullanıcı adı ve şifre ile giriş yapar.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Ürün listesinin yüklenmesini bekler ve bir ürüne tıklar.
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        product_link.click()

        # Sepete ekleme butonuna tıklar.
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn_primary.btn_inventory"))
        )
        add_to_cart_button.click()

        # Sepete giderek ödeme işlemine başlar.
        cart_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_icon.click()

        checkout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        )
        checkout_button.click()

        # Ödeme bilgilerini doldurur ve işlemi tamamlar.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()

        # Ödeme işleminin tamamlandığını doğrular.
        finish_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "finish"))
        )
        finish_button.click()

        # Sonucun doğruluğunu kontrol eder.
        # Sınıfı "complete-header" olan elementin metnini doğrular.
        complete_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert complete_header.text == "Thank you for your order!"

    except Exception as e:
        # Hata durumunda ekran görüntüsü alır.
        driver.save_screenshot('test_checkout_error.png')
        raise e
