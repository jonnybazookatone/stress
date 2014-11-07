"""Base class of stress testing"""
import time
import logging
import sys
from logging.handlers import RotatingFileHandler
from selenium.webdriver import Firefox as ffx
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb

__author__ = "Jonny Elliott"

class WebPage(ffx):
  
  def __init__(self, url, headless=False):

    if headless:
      self.makeHeadLess()

    ffx.__init__(self)
    self.url = url
    self.minimum_timeout = 60
    self.headless = headless
    self.timed_out = False

    self.load_time = -99
    self.login_time = -99
    self.logout_time = -99

    # Logging
    logfmt = '%(levelname)s [%(asctime)s]:\t  %(message)s'
    datefmt= '%m/%d/%Y %I:%M:%S %p'

    formatter = logging.Formatter(fmt=logfmt,datefmt=datefmt)
    self.logger = logging.getLogger('__main__')

    logging.root.setLevel(logging.DEBUG)
    rfh = RotatingFileHandler(filename="/diska/home/jonny/sw/python/stress/stress/gp_timings.log",maxBytes=1048576,backupCount=3,mode='a')
    rfh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    self.logger.handlers = []
    self.logger.addHandler(ch)
    self.logger.addHandler(rfh)

  def makeHeadLess(self):
    self.xvfb = Xvfb(width=1280, height=720)
    self.xvfb.start()
    self.headless = True

  def pageLoad(self, wait=False):

    self.logger.info("Loading page.")
    
    start_time = time.time()
    self.get(self.url)

    if wait:
      try:
        element = WebDriverWait(self, self.minimum_timeout).until(EC.presence_of_element_located((By.ID, wait)))

      except TimeoutException:
        self.logger.warning("TimeoutException thrown. Continuing.")
        self.timed_out = True

      except:
        self.logger.error("Unexpected behaviour. Terminating.")
        sys.exit()

    end_time = time.time()

    self.load_time = end_time - start_time
     
    self.logger.info("Page loaded successfully.")


  def findAndClick(self, value, by=By.ID):
    self.find_element(by=by, value=value).click()

  def pageLogin(self, username="test", password="test", 
                      username_value="test", password_value="test", login_value="test",
                      wait=False):

    self.logger.info("Logging into page.")

    username_element = self.find_element(by=By.ID, value=username_value)
    password_element = self.find_element(by=By.ID, value=password_value)

    username_element.send_keys(username) 
    password_element.send_keys(password)

    start_time = time.time()
    self.findAndClick(login_value)
    
    if wait:
      try:
        element = WebDriverWait(self, self.minimum_timeout).until(EC.presence_of_element_located((By.ID, wait)))
      except TimeoutException:
        start_time = 0
        self.logger.warning("TimeoutException thrown. Continuing.")
      except: 
        self.logger.error("Unexpected behaviour. Terminating.")
        sys.exit()

    end_time = time.time()
    self.login_time = end_time - start_time
   
    self.logger.info("Page logged into sucessfully.")
 
  def pageLogout(self, logout_value="tool-exit", confirm_value="//button[text()=\"Yes\"]", wait=False):

    self.logger.info("Logging out of page.")

    start_time = time.time()
    self.findAndClick(value=logout_value)
    self.findAndClick(value=confirm_value, by=By.XPATH)
    if wait:
      try:
        element = WebDriverWait(self, self.minimum_timeout).until(EC.presence_of_element_located((By.ID, wait)))
      except TimeoutException:
        start_time = 0
        self.logger.warning("TimeoutException thrown. Continuing.")
      except:
        self.logger.error("Unexpected behaviour. Terminating.")
        sys.exit()

    end_time = time.time()
 
    self.logout_time = end_time - start_time
   
    self.logger.info("Page logged out successfully.")

  def quit(self):
    if self.headless:
      self.xvfb.stop()
    super(WebPage, self).quit()
