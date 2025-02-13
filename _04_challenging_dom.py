import unittest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ChallengingDomTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome driver ONCE AND SHARE it resources for all tests
        s = Service(executable_path='./chromedriver')
        cls.driver = webdriver.Chrome(service=s)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
    
    def setUp(self):
        # Open the target webpage before each test method
        self.driver.get("https://the-internet.herokuapp.com/challenging_dom")
        # Giving a little time to load
        time.sleep(1)
        
    def test_challenging_dom(self):
        driver = self.driver
        wait = self.wait
        get_btns = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.large-2.columns a')))
        colors = []
        
        for i in range(len(get_btns)):
            relocation = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.large-2.columns a')))
            
            # Re-locate the button to avoid stale exception
            btn = wait.until(EC.element_to_be_clickable(relocation[i]))

            background_color = btn.value_of_css_property('background-color')  # Get background color
            if not background_color in colors:
                # Try to click the btn
                try:
                    btn.click()
                    colors.append(background_color)
                except:
                    self.fail(f"Error while clicking on the button with color: , {background_color}")
                
                # Search and Checking if the Canvas is displayed
                try:
                    canvas = wait.until(EC.presence_of_element_located((By.ID,'canvas')))
                    canvas_displayed = canvas.is_displayed()
                    if not canvas_displayed:
                        self.fail(f"Error while clicking on the button with color: , {background_color}")
                        
                except:
                    self.fail(f"No canvas displayed after button clicked")
            else:
                self.fail(f"Button repeated, {background_color}")
       
        logging.info("test_challenging_dom -> Test passed!")

    def test_table_info(self):
        driver = self.driver
        
        print("getting the table information")
        print('---'*10)

        get_thead_elements = driver.find_elements(By.XPATH,"//thead/tr/th")
        get_tbody_tr_elements = driver.find_elements(By.XPATH,"//tbody/tr")

        header_expected = ['Lorem', 'Ipsum', 'Dolor', 'Sit', 'Amet', 'Diceret', 'Action']
        header = []
        for row in get_thead_elements:
            header.append(row.text)

        self.assertEqual(header_expected,header, f"Expected {header_expected}, but got: {header}")
        
        row = 0
        for b_row in get_tbody_tr_elements:
            row += 1
            try:
                get_td_elements = b_row.find_elements(By.TAG_NAME,'td')
            except:
                self.fail("NO row elements found with tag <td>")
            if get_td_elements:
                # arr_data = [ele.text for ele in get_td_elements]
                # print(row,arr_data)
                
                # Now try to clicking the 2 <a> url in each row element
                links_col = get_td_elements[-1]
                try:
                    links = links_col.find_elements(By.TAG_NAME,'a')
                except:
                    self.fail("NO url found with tag <a>")
                    
                for link in links:
                    try:
                        # print(f'Link text= {link.text}, HREF: {link.get_attribute("href")}')
                        link.click()
                    except:
                        self.fail("Error while clicking the URL element")

        logging.info("test_table_info -> Test passed!")
        
    
    # Cleaning the driver
    @classmethod
    def tearDownClass(cls):
        logging.info("Closing browser session")
        time.sleep(1)
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)