import unittest
import time
from python.stress.stress.stress import WebPage

class Test(unittest.TestCase):

  def test_load_page(self):
    myPage = WebPage("http://www.google.de")
    myPage.pageLoad()
    self.assertEqual("Google", myPage.title)
    myPage.quit()
    time.sleep(5) # Ensure do not spam google during testing

  def test_timing_load_page(self):
    myPage = WebPage("http://www.google.de")
    myPage.pageLoad()
    self.assertTrue(myPage.load_time > 0)
    myPage.quit()
    time.sleep(5)

  def test_timing_login_fail(self):
    myPage = WebPage("https://accounts.google.com/ServiceLogin?sacu=1")
    myPage.pageLoad()
    myPage.pageLogin(username="test", password="test", 
                     username_value="Email", password_value="Passwd", login_value="signIn")
    
    fail_text = myPage.find_element_by_id("errormsg_0_Passwd").text
    self.assertTrue("The email or password you entered is incorrect." in fail_text)
    myPage.quit()
    time.sleep(5)

  def test_waiting(self):
    myPage = WebPage("http://www.google.de")
    myPage.pageLoad(wait="gibberish")
    myPage.quit()
    self.assertTrue(myPage.load_time > 10)
    time.sleep(5)

  def test_find_and_click(self):
    myPage = WebPage("http://www.google.de")
    myPage.pageLoad()
    myPage.findAndClick("gb_70")
    #myPage.findAndClick("account-chooser-add-account")
    success_text = myPage.find_element_by_class_name("banner").text
    self.assertTrue("Einmal anmelden." in success_text)
    myPage.quit()
    time.sleep(5)

  def test_timing_logout_page(self):
    myPage = WebPage("http://google.de")
    myPage.pageLoad()
    myPage.pageLogout(logout_value="gbqfba", confirm_value="//button[@id=\"gbqfbb\"]", wait="logo")
    myPage.quit()
    time.sleep(5)
