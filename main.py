import time
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# require accpw.py and json that contain account and password
from accpw import fetchFrom


class Beanfun():
    def __init__(self):
        self.web = webdriver.Firefox()
        self.web.install_addon('beanfun.xpi', temporary=True)
        self.web.get('https://tw.beanfun.com/')

        self.find = self.web.find_element

    def wait_until_found(self, element: str, timeout: float = 10, by=By.ID):
        return WebDriverWait(self.web, timeout).until(
            lambda x: x.find_element(by, element)
        )

    def login(self):
        self.find(By.ID, 'BF_anchorLoginBtn').click()
        frame = self.wait_until_found('ifmForm1')
        self.web.switch_to.frame(frame)

        acc, pw = fetchFrom('Beanfun')
        accid = self.wait_until_found('t_AccountID')
        accid.send_keys(acc)
        self.find(By.ID, 't_Password').send_keys(pw)
        self.find(By.ID, 'btn_login').click()

        WebDriverWait(self.web, 30).until(
            lambda x: x.current_url == 'https://tw.beanfun.com/'
        )

    def login_game(self):
        self.web.get('https://tw.beanfun.com/game_zone/')
        self.find(By.ID, 'BF_btnQuickStart').click()
        self.find(By.ID, 'BF_BaseList').find_element(By.TAG_NAME, 'li').click()
        frame = self.wait_until_found('fbContent')
        self.web.switch_to.frame(frame)

        try:
            never_remind = WebDriverWait(self.web, 10).until(
                EC.element_to_be_clickable(self.find(By.ID,
                                                     'cbxRemoveServiceFriendlyReminder')))
            if not never_remind.is_selected():
                never_remind.click()
            time.sleep(6)
            self.find(By.ID, 'btnFriendlyReminderOK').click()

        except NoSuchElementException as e:
            print(e)

    def start(self):
        self.login()
        self.login_game()
        time.sleep(20)
        self.web.close()


Beanfun().start()
