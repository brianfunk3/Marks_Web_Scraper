from utils import buildHeadless
from seleniumHandlers import getBy
import time

def login(driver, email, password):
    """this function logs us in to the music league website"""
    # navigate to the root page
    driver.get('https://app.musicleague.com/')

    # find initial login button and click
    result = getBy(driver, 'class', 'loginButton')
    result.click()

    # let sleep for full load just in case - I think this is unecessary?
    time.sleep(3)

    # send username
    username_button = getBy(driver, 'id', 'login-username')
    username_button.send_keys(email)

    time.sleep(5)

    # send password
    password_button = getBy(driver, 'id', 'login-password')
    password_button.send_keys(password)

    # now log in!
    login_button = getBy(driver, 'id', 'login-button')
    login_button.click()

    # wait a few seconds again
    time.sleep(3)

    # apparently the "agree" button pops up everytime cause my virtual browser doesn't have cookies
    # if yours works differently, can comment this out
    agree_button = getBy(driver, 'class', 'Button-qlcn5g-0')
    agree_button.click()

    # wait yet again
    time.sleep(3)

    return


def main():
    # build our headless driver
    driver = buildHeadless()

    # attempt to pull in credentials
    with open('credentials.txt', 'r') as f:
        email = f.readline().strip()
        password = f.readline().strip()

    # log in to the website
    login(driver, email, password)
    
    # bye
    driver.close()

main()