from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import seleniumHandlers

def buildHeadless():
    options = ChromeOptions()
    #options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.set_page_load_timeout(5)

    return driver