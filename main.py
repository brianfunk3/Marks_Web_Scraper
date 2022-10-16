from utils import buildHeadless
from seleniumHandlers import getBy
import time

def main():
    # build our headless driver
    driver = buildHeadless()

    # navigate to a webpage
    driver.get('https://app.musicleague.com/')

    # look for the button
    result = getBy(driver, 'class', 'loginButton')

    # press button
    result.click()

    # let sleep for full load just in case - I think this is unecessary?
    time.sleep(3)

    # send username
    username = getBy(driver, 'id', 'login-username')
    username.send_keys('HOWDY')

    #

    # bye
    driver.close()

main()