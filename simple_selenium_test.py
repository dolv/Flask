from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import unittest


profile = webdriver.FirefoxProfile('F:\\Programming\\Dolv\\IdeaProjects\\ffprofile')
driver = webdriver.Firefox(profile)
#driver.manage().window().maximize();
#driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
baseURL = "http://localhost:5000/"
driver.get(baseURL)
