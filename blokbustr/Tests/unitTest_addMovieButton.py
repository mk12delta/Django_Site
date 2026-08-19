import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.byimport By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        user = "localsuperuser"
        pwd = "lSU-PASSWORD"
        driver.get("http://127.0.0.1:8000/accounts/login/")
        time.sleep(3)
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:8000/movies/")
        time.sleep(3)
        # find 'Add Movie Button' and click it to ensure screen advances to Add Movie page.
        driver.find_element(By.XPATH, "/html/body/nav/div/div/ul[1]/li[2]/a").click()

        time.sleep(5)
        try:
            # Verify clicked review button returns the reviews page

            elem = driver.find_element(By.LINK_TEXT, "Add Movie")
            self.driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Page Does Not Advance to Add Movie Page")


time.sleep(2)


def tearDown(self):
    self.driver.quit()


if __name__ == "__main__":
    unittest.main()