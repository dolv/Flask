from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
from flask import Flask
from flask_testing.utils import TestCase
from flask_testing import LiveServerTestCase
import unittest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC

class MyTest(unittest.TestCase):
#class MyTest(LiveServerTestCase):

    def setUp(self):
        self.profile = webdriver.FirefoxProfile('F:\\Programming\\Dolv\\IdeaProjects\\ffprofile')
        binary = FirefoxBinary('c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
        self.driver = webdriver.Firefox(self.profile, firefox_binary=binary)
        self.baseURL = "http://127.0.0.1:5000/"

    def tearDown(self):
        self.driver.quit()

    def test_url_shortener(self):
        self.driver.get(self.baseURL)
        element = self.driver.find_element(by='xpath', value="//input[@name='url']")
        element.send_keys("http://example.com")
        element.send_keys(Keys.RETURN)
        self.driver.get(self.driver.current_url+'qwefqwef')
        self.assertTrue(self.driver.current_url == self.baseURL)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
