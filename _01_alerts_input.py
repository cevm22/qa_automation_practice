import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class AlertsInputTest(unittest.TestCase):
    
    def setUp(self):
        # Set up the Chrome driver
        s = Service(executable_path='./chromedriver')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver
        
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        # Open the target webpage
        driver.get("https://the-internet.herokuapp.com/javascript_alerts")
        driver.maximize_window() 
        # Giving a little time to load
        time.sleep(3)
    
    
    def test_alert_dismiss(self):
        driver = self.driver
        wait = self.wait
        
        input_text = "THIS IS A TEST INPUT SEND KEYES"
        js_confirmation = wait.until(EC.presence_of_element_located((By.XPATH,"//button[text()='Click for JS Prompt']")))
        js_confirmation.click()
        
        # switching the browser to Alert popup
        alert = driver.switch_to.alert
        
        # Send input text
        alert.send_keys("THIS IS A TEST INPUT SEND KEYES")
        
        # Accept the input
        alert.accept()
        
        text_result = wait.until(EC.presence_of_element_located((By.XPATH,"//p[@id='result']")))
        
        concat = f'You entered: {input_text}'

        self.assertEqual(concat, text_result.text, f"Expected '{concat}' but got '{text_result.text}'")
        # Accept the input prompt
        time.sleep(3)
        
        logging.info("test_alert_dismiss -> Test passed!")

        
    # Cleaning the driver
    def tearDown(self):
        logging.info("Closing browser session")
        time.sleep(1)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)