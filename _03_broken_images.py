import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BrokenImagesTest(unittest.TestCase):
    
    def setUp(self):
        # Set up the Chrome driver
        s = Service(executable_path='./chromedriver')
        self.driver = webdriver.Chrome(service=s)
        driver = self.driver
        
        self.wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        # Open the target webpage
        driver.get("https://the-internet.herokuapp.com/broken_images")
        driver.maximize_window() 
        # Giving a little time to load
        time.sleep(1)
        
    def test_broken_images(self):
        driver = self.driver
        wait = self.wait
        
        get_images = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,"img")))
        print("images found: ",len(get_images))
        
        # To know if an image is broken, is needed to ask to the server by its src.
        for image in get_images:
            src = image.get_attribute('src')
            try:
                # asking to server with timeout of 5 secs
                response = requests.get(src,timeout=5)
                # status_code = 200 #fixed situation when all exists
                status_code = response.status_code
                
                if status_code >= 400:
                    logging.error(f"Broken image detected: {src} (Status Code: {status_code})")
                    self.fail(f"Broken image: {src} (Status Code: {status_code})") 
                    
                else:
                    logging.info(f"Valid image: {src} (Status Code: {status_code})")

            
            except Exception as e:
                logging.error(f"Error checking image {src}: {e}")
                self.fail(f"Failed to check image {src}: {e}")
        
    # Cleaning the driver
    def tearDown(self):
        logging.info("Closing browser session")
        time.sleep(1)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)