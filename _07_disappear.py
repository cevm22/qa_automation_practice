import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DisappearTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/disappearing_elements")
        # Giving a little time to load
        time.sleep(1)
        
    def test_disappear(self):
        driver = self.driver
        wait = self.wait
        
        attempts = 0
        max_attempts = 10
        for _ in range(max_attempts):
            headers = self.retrive_headers()
            attempts += 1
            if len(headers) == 5:
                # print("All headers present")
                break
            driver.refresh()
            # print("giving some time to see the elements")
            # time.sleep(1)
        if attempts >= max_attempts:
            self.fail(f"Missing headers after max_attempts > {max_attempts}")
        # print("total attempts befor get expected headers ",attempts)
        
        # Last check if the menu items are available and displayed in the UI
        self.check_menu_items()
        logging.info("test_disappear -> Test passed!")
        

    def retrive_headers(self):
        wait = self.wait
        try:
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//ul/li')))
        except:
            self.fail("Error while looking for the headers")
        headers = []
        for index, element in enumerate(elements):
            # print("index: ",index,"element: ", element.text)
            headers.append(element.text)
        return headers
    
    def check_menu_items(self):
        wait = self.wait
        try:
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//ul/li')))
        except:
            self.fail("Error while looking for the headers")
        for el in elements:
            is_displayed = el.is_displayed()
            is_enabled = el.is_enabled()
            if not is_displayed or not is_enabled:
                self.fail("Some menu component is not enabled or displayed")
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)