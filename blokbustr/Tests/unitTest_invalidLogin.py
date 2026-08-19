# Unit test file which verifies the /accounts/login page prevents user from logging
# in when invalid user credentials are used, and still displays the ‘Login’ and ‘Sign Up’
# tabs at the top of the screen, confirming the user did not successfully login.

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.byimport By
from selenium.webdriver.support.ui import WebDriverWait


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)  # wait 5 seconds for home page

    def test_ll(self):
        # Incorrect username/password to test if failed login with message works
        # as intended and passes this unitTest. The Correct combination is "ericm/lhBanjo1$"
        user = "testuser5"
        pwd = "test1235"

        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/accounts/login/")

        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)

        try:
            elements = driver.find_elements(By.XPATH, "/html/body/nav/div/div/ul[2]/li/form/button")

            if elements:
                assert False
            else:
                assert True

        except NoSuchElementException:
            assert True

        def tearDown(self):
            self.driver.quit()

        if __name__ == "__main__":
            unittest.main(warnings='ignore')

if __name__ == "__main__":
    unittest.main(warnings='ignore')