from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from memorysolver import MemorySolver

class bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def login(self):
        self.driver = webdriver.Chrome('./ChromeDriver/chromedriver.exe')
        # go to the login page
        self.driver.get('https://www.swagbucks.com/p/login')

        # get the fields
        emailField = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_id('sbxJxRegEmail'))
        passField = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_id('sbxJxRegPswd'))

        # enter the credentials
        emailField.send_keys(self.username)
        passField.send_keys(self.password)

        # switch to the captcha frame and click the captcha
        captchaFrame = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_xpath('//*[@id="sbCaptcha"]/div/div/iframe'))
        self.driver.switch_to_frame(captchaFrame)
        captchaBox = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[5]'))
        captchaBox.click()

        print('Now please complete the captcha and hit enter.')
        input()

        # now hit the login button
        self.driver.switch_to_default_content()
        passField.submit()

    def search_for(self, text):
        # get the search field, enter the text and submit
        searchField = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_id('sbGlobalNavSearchInputWeb'))
        searchField.clear()
        searchField.send_keys(text)
        try:
            self.driver.find_element_by_id('topWinMsg')
            print('Search successful! Solve the captcha and hit enter.')
            input()
        except:
            print('Search unsuccessful.')
        try:
            # the annoying rule guy
            self.driver.find_element_by_id('rulesTooltip')
            sleep(3)
        except:
            pass

    def search_for_all(self, elements):
        for curElement in elements:
            self.search_for(curElement)

    def solve_memory(self):
        self.driver.get('http://www.swagbucks.com/games/play/116/swag-memory')
        start_game = WebDriverWait(self.driver, 10).until(lambda d: d.find_element_by_id('gamesItemBtn'))
        start_game.click()
        solver = MemorySolver()
        sleep(5)
        #print(solver.locate('img/memory.png'))
        solver.solve()
        sleep(2)
        # close the extra window if it still exists
        base_handle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != base_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()
                self.driver.switch_to.window(base_handle)

if __name__ == '__main__':
    swagbot = bot('efa87575@tiapz.com', 'Rz3v6e8t')
    swagbot.login()
    while True:
        swagbot.solve_memory()
