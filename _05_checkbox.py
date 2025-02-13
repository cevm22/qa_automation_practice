import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class CheckboxesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/checkboxes")
        # Giving a little time to load
        time.sleep(1)
        
    def test_checkboxes(self):
        driver = self.driver
        wait = self.wait
        try:
            get_checkboxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'input[type="checkbox"]')))
        except:
            self.fail("checkboxes NOT FOUND")
        
        print("Checkboxes: ",len(get_checkboxes))
        
        if not len(get_checkboxes) == 2: self.fail(f"Expected 2 checkboxes, but got {len(get_checkboxes)}")
        
        for index, checkbox in enumerate(get_checkboxes):
            is_enabled = checkbox.is_enabled()
            if not is_enabled: self.fail(f'checkbox number {index} is not enabled')
    
            try:
                checkbox.click()
            except:
                self.fail("Impossible to click the checkbox")
        
        try:
            retrive_checkboxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'input[type="checkbox"]')))
            box_1 = retrive_checkboxes[0].is_selected()
            box_2 = retrive_checkboxes[1].is_selected()
        except:
            self.fail("checkboxes NOT FOUND in the second check")
            
        self.assertTrue(box_1,"checkbox 1 expected SELECTED")
        self.assertFalse(box_2,"checkbox 2 expected !NOT! SELECTED")
        logging.info("test_checkboxes -> Test passed!")
        
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)