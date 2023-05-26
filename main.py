from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import random

class Bot():
  def __init__(self, poll_name, email, netid, password, default_timeout, interval):
    """
    Handles initializing a Bot instance

    poll_name: the polleve poll name
    email: uw student email
    netid: uw netid
    password: uw student password
    default_timeout: the amount of time in ms to allow for searching for an
      elementbefore throwing an exception 
    interval: the interval at which to poll the polleve
    """
    self.driver =  webdriver.Firefox()
    self.poll_name = poll_name
    self.email = email
    self.netid = netid 
    self.password = password
    self.default_timeout = default_timeout
    self.interval = interval
  

  def login(self):
    """
    Handles logging into a polleve account. Requires that the credentials are 
    a UW student (it is unlikely that the webflow is similar across
    different colleges).
    """
    print("logging in...")
    self.driver.get('https://id.polleverywhere.com/login')

    print("entering email to email input")
    email_input = self.driver.find_element(By.XPATH, '//*[@id="username"]')
    email_input.send_keys(f"{self.email}")

    print("sending click to next")
    next_btn = self.driver.find_element(By.CSS_SELECTOR, "#sign_in_form > form > div > button")
    next_btn.click()

    print("sending click to LoginWithUW")
    uw_btn = self.driver.find_element(By.CSS_SELECTOR, "#sign_in_form > div > form:nth-child(2) > button")
    uw_btn.click()

    print("entering netid to netid input")
    netid_input = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#weblogin_netid')))
    netid_input.send_keys(f"{self.netid}")

    print("entering password to password input")
    password_input = self.driver.find_element(By.CSS_SELECTOR, '#weblogin_password')
    password_input.send_keys(f"{self.password}")

    print("sending click to login")
    login = self.driver.find_element(By.CSS_SELECTOR, "#submit_button")
    login.click()

    print("waiting for 2FA")

    # wait for pollev page to load
    WebDriverWait(self.driver, self.default_timeout).until(lambda driver: "https://pollev.com" in driver.current_url)

    print("already signed in poll ev")

    # goto poll ev homepage
    self.driver.get("https://pollev.com/home")

    # get the pollname input
    pollname_input = WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pe-text-field__input")))
    pollname_input.send_keys(f"{self.poll_name}")

    # click the join btn
    join_btn = self.driver.find_element(By.CSS_SELECTOR, ".pollev-home-join__submit")
    join_btn.click()

  def poll_mc(self):
    """
    Periodically (specified in self.interval) sends a click to a polleve 
    multiple choice component. 
    """
    while True:
      try:
        print("waiting for mc...")
        # wait for at least found one
        WebDriverWait(self.driver, self.default_timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'component-response-multiple-choice__option__value')))
        # find elements instead of just one, a list is returned
        mc_list = self.driver.find_elements(By.CLASS_NAME, "component-response-multiple-choice__option__value")
        assert len(mc_list) > 0
        # randomly pick one choice to vote for
        mc = random.choice(mc_list)
        mc.click()
        print("sending click to mc")

        print("pausing search...")
        time.sleep(self.interval)

      except Exception as e:
        print ('Exception type is:', e.__class__.__name__)
      
      
  def end_session(self):
    """
    Terminates the webdriver (self.driver)
    """
    print("closing...")
    self.driver.close()
    print("successfully closed")
    

class Credentials():
  def __init__(self):
    print("looking for a credential file...")

    if not self.is_credential_valid():
      print("credential file doesn't exist \n creating credential file")
      self.create_credential()
    else:
      print("credential file already exists")
    
    print("reading credential contents...")
    credentials = self.read_credentials()

    self.poll_name = credentials["poll_name"]
    self.email = credentials["email"]
    self.netid = credentials["netid"]
    self.password = credentials["password"]
    self.default_timeout = credentials["default_timeout"]
    self.interval = credentials["interval"]


  def read_credentials(self):
    """
    Reads credential.txt and returns its contents as a JSON. Requires the contents
    of credentials.txt
    """
    with open("credentials.txt", "r") as f:
      contents = f.read()
      credentials = json.loads(contents)
      return credentials
  

  def is_credential_valid(self):
    """
    Returns whether a credential file exists in path
    """
    return os.path.isfile("./credentials.txt")
  

  def create_credential(self):
    """
    Creates a credential file based on user input
    """
    with open('credentials.txt', "w") as f:
      poll_name = input("poll name: ")
      email = input("email: ") 
      netid = input("netid: ")
      password = input("password: ")
      default_timeout = input("default timeout: ")
      interval = input("interval: ")
      credentials = {
        "poll_name": poll_name, 
        "email": email,
        "netid": netid,
        "password": password,
        "default_timeout": default_timeout,
        "interval": interval
      }
      f.write(json.dumps(credentials))
      print("created credentials file")
  

if __name__ == "__main__":
  cred = Credentials()
  bot= Bot(
    poll_name=cred.poll_name, 
    email=cred.email,
    netid=cred.netid,
    password=cred.password,
    default_timeout=int(cred.default_timeout),
    interval=int(cred.interval)
  )

  try:
    bot.login()
    bot.poll_mc()
  except Exception as e:
    print("an error occurred")
    print(e)
    print("hit any key to end program")
  
  bot.end_session()
  

