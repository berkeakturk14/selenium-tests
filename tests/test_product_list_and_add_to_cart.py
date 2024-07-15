import pytest  # PyTest kütüphanesi, testlerinizi organize etmenizi ve çalıştırmanızı sağlar.
from selenium import webdriver  # Selenium WebDriver, tarayıcıları otomatik olarak kontrol etmenizi sağlar.
from selenium.webdriver.common.by import By  # Elementleri bulmak için farklı stratejiler sağlar.
from selenium.webdriver.chrome.service import Service  # ChromeDriver servisini yönetir.
from selenium.webdriver.support.ui import WebDriverWait  # Web elementlerinin yüklenmesini beklemek için kullanılır.
from selenium.webdriver.support import expected_conditions as EC  # Bekleme koşulları için kullanılır.

# ChromeDriver'ın tam yolunu belirtin
chrome_driver_path = "C:/Program Files (x86)/chromedriver/chromedriver.exe"  # ChromeDriver'ın bulunduğu yol.
service = Service(executable_path=chrome_driver_path)  # ChromeDriver servis nesnesi oluşturulur.

@pytest.fixture(scope="module")  # Bu, bir PyTest fixture'ıdır ve test modülü boyunca bir kez çalıştırılır.
def driver():
    driver = webdriver.Chrome(service=service)  # Chrome WebDriver nesnesi oluşturulur.
    yield driver  # Bu, test fonksiyonuna WebDriver'ı sağlar ve test bittikten sonra driver.quit() çalışır.
    driver.quit()  # Testler bittikten sonra tarayıcıyı kapatır.

def test_product_search(driver):
    driver.get("https://www.saucedemo.com")  # saucedemo'ya gidin.
    driver.maximize_window()  # Tarayıcıyı tam ekran yapın.
    driver.find_element(By.ID, "user-name").send_keys("standard_user")  # Kullan
    driver.find_element(By.ID, "password").send_keys("secret_sauce")  # Kullan
    driver.find_element(By.ID, "login-button").click()  # Giriş yapın

     # Ürün listesinin yüklenmesini bekler.
    product_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
    assert len(product_list) > 0 # Ürün listesinin 0 dan fazla ürün içerdiği doğrular
    
    first_product_add_to_cart_button = product_list[0].find_element(By.CLASS_NAME,"btn_inventory")
    first_product_add_to_cart_button.click()  # İlk ürünü sepete ekleyin.

    cart_badge = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    ).text
    assert cart_badge == "1" #eger sepet guncellenmemisse test basarisiz olur.
