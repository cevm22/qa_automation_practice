import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ContextMenuTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/context_menu")
        # Giving a little time to load
        time.sleep(1)
        
    def test_context_menu(self):
        driver = self.driver
        wait = self.wait

        # Getting the hotspot to activate the contentext menu
        try:
            hotspot = wait.until(EC.presence_of_element_located((By.ID, "hot-spot")))
        except:
            self.fail("Hotspot NOT FOUND")
        # create actions chains to simulate rightclick  where is located the hotspot
        actions = ActionChains(driver)
        actions.context_click(hotspot).perform()  # Simulate right-click
        
        try:
            # Wait for the alert to be present
            alert = wait.until(EC.alert_is_present())
            
            # Get the alert text
            alert_text = alert.text
            
            # Validate the alert text
            expected_text = "You selected a context menu"
            self.assertIn(expected_text,alert_text, f"Expected {expected_text}, but got {alert_text}")
            
            # Accept the alert popup 
            alert.accept()
            logging.info("test_context_menu -> Test passed!")
            
        except Exception as e:
            self.fail("Something went wrong while clicking on hotspot")
        
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)