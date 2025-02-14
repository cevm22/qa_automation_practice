import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DragAndDropTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.download_path = os.path.abspath("./downloads")  

        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/drag_and_drop")
        # Giving a little time to load
        time.sleep(1)
        
    def test_drag_and_drop(self):
        driver = self.driver
        wait = self.wait
        
        # before perform drag n drop
        try:
            side_a = wait.until(EC.presence_of_element_located((By.ID,"column-a")))
            side_b = wait.until(EC.presence_of_element_located((By.ID,"column-b")))
        except:
            self.fail("COLUMNS NOT FOUND")
        
        try:
            actions = ActionChains(driver)
            actions.drag_and_drop(side_a,side_b).perform()
        except:
            self.fail("Error while performing drag and drop")
        
        try:    
        # get the texts of the columns to compare them
            left = wait.until(EC.text_to_be_present_in_element((By.ID, "column-a"), "B"))
            right = wait.until(EC.text_to_be_present_in_element((By.ID, "column-b"), "A"))
        except:
            self.fail("COLUMNS NOT FOUND")
        
        # Validate the elements were swapped
        self.assertTrue(right, f"Expected A but got: {side_b.text}")
        self.assertTrue(left, f"Expected B but got: {side_a.text}")
        logging.info("test_drag_and_drop -> Test passed!")

            
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)