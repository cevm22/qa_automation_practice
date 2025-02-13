import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BasicAuthTest(unittest.TestCase):
    
    def setUp(self):
        # Set up the Chrome driver
        s = Service(executable_path='./chromedriver')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver
        
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        
    
    
    def test_basic_auth(self):
        driver = self.driver
        wait = self.wait
        username = "admin"
        password = "admin"
        url = f"https://{username}:{password}@the-internet.herokuapp.com/basic_auth"
        
        # Open the target webpage
        driver.get(url)
        driver.maximize_window() 
        # Giving a little time to load
        time.sleep(1)
        # look for congrats msg
        success_message = driver.find_element(By.TAG_NAME, "p").text
        self.assertIn("Congratulations!",success_message, "Authentication failed or page content is incorrect.")
        logging.info("test_basic_auth -> Test passed!")
 
        
        
    # Cleaning the driver
    def tearDown(self):
        logging.info("Closing browser session")
        time.sleep(1)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)