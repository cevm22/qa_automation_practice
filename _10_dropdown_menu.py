import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DropdownMenuTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        # Giving a little time to load
        time.sleep(1)
        
    def test_dropdown_menu(self):
        driver = self.driver
        wait = self.wait
        try:
            # get_dropdown = driver.find_element(By.ID,"dropdown") # OR
            get_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"select")))
            dropdown = Select(get_dropdown)
        except:
            self.fail("Dropdown NOT FOUND")

        list_expected = ['Please select an option', 'Option 1', 'Option 2']
        dropdown_list = []
        # print all the options
        for option in dropdown.options:
            dropdown_list.append(option.text)
         
        self.assertEqual(list_expected,dropdown_list, "Dropdown items are missing")
        
        # Select option 2 by it text instead position
        dropdown.select_by_visible_text("Option 2")
        selected_option = dropdown.first_selected_option.text
        
        # Validate the current selection is what we expected
        self.assertEqual(selected_option,"Option 2", f"Wrong selected item from dropdown expected: Option 2, got:  {selected_option}")
         
        logging.info("test_dropdown_menu -> Test passed!")

            
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)