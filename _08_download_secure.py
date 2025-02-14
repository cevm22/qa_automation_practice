import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DownloadSecureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.download_path = os.path.abspath("./downloads")  
        # Configure Chrome options to handle downloads
        options = Options()
        prefs = {
            "download.default_directory": cls.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s, options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/download_secure")
        # Giving a little time to load
        time.sleep(1)
        
    def test_download_secure(self):
        driver = self.driver
        wait = self.wait
        try:
            print("trying download without auth")
            links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'a')))
            if links: self.fail("Expected no links available without auth")
        except Exception as e:
            logging.info("Checked links cant be availabe without auth")
            
        username = "admin"
        password = "admin"
        url = f"https://{username}:{password}@the-internet.herokuapp.com/download_secure"
        driver.get(url)
        time.sleep(1)
        # links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'a')))
        # print(len(links))
        try:
            # Get file to download it 
            file_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='download_secure/some-file.txt']")))
            # Click the download link
            file_link.click()
        except:
            self.fail("Download URL not found")
            
        # Verify the download
        downloaded_file_path = os.path.join(self.download_path, "some-file.txt")
        
        try:
            WebDriverWait(driver,30).until(lambda _: os.path.exists(downloaded_file_path))
            logging.info("test_download_secure -> Test passed!")
        except:
            self.fail(f"File downloaded not found on path expected {self.download_path}/some-file.txt but got {downloaded_file_path}")
      
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)