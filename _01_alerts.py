import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AlertsTest(unittest.TestCase):
    
    def setUp(self):
        # Set up the Chrome driver
        s = Service(executable_path='./chromedriver')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver
        
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        # Giving a little time to load
        driver.implicitly_wait(3)
        # Open the target webpage
        driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    
    def test_alert(self):
        driver = self.driver
        wait = self.wait
        
        expected_text = "I am a JS Alert"
        js_alert = wait.until(EC.presence_of_element_located((By.XPATH,"//button[text()='Click for JS Alert']")))
        js_alert.click()
        # switching the browser to Alert popup
        alert = driver.switch_to.alert
        
        # print("JS alert text > ", alert.text)
        self.assertEqual(alert.text, expected_text, f"Expected '{expected_text}' but got '{alert.text}'")

        # Accepting the ok btn from alert
        alert.accept()
        logging.info("test_alert -> Test passed!")
        
        
    # Cleaning the driver
    def tearDown(self):
        logging.info("Closing browser session")
        time.sleep(1)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)