from seleniumHandlers import getBy
from selenium.webdriver.common.by import By

import time
from random import randint

# how many rounds we up to these days?
round_count = 11

def rand_wait(bot = 3, top = 7):
    """get a random time to wait between two integers. defaults to 3 and 7 seconds"""
    return randint(bot, top)

def login(driver, email, password):
    """this function logs us in to the music league website"""
    # navigate to the root page
    driver.get('https://app.musicleague.com/')

    # find initial login button and click
    getBy(driver, 'class', 'loginButton').click()

    # let sleep for full load just in case - I think this is unecessary?
    time.sleep(rand_wait())

    # send username
    getBy(driver, 'id', 'login-username').send_keys(email)

    # send password
    getBy(driver, 'id', 'login-password').send_keys(password)

    # now log in!
    getBy(driver, 'id', 'login-button').click()

    # wait a few seconds again
    time.sleep(rand_wait())

    # apparently the "agree" button pops up everytime cause my virtual browser doesn't have cookies
    agree_button = getBy(driver, 'class', 'Button-qlcn5g-0')
    if agree_button: agree_button.click()

    # wait yet again, make this one a bit longer though
    time.sleep(rand_wait(bot = 5))

    # get rid of that stupid reminder box, if it exists
    close_button = getBy(driver, 'class', 'btn-close')
    if close_button: close_button.click()

    # wait wait wait
    time.sleep(rand_wait())

    return

def pull_data(driver):
    """function that takes in a logged-in browser state and pulls each week of data
    data gets saved out to html files in the /tmp/ directory"""
    # navigate to my league
    # TODO: allow people to pass in their own leagues
    league_button = getBy(driver, 'css', "a[title*='Musicverse of Madness']")
    league_button.click()

    # wait for it to load
    time.sleep(rand_wait())

    # pull the div that includes all the weeks
    all_rounds = getBy(driver, 'class', 'py-5')

    # now try and pull all of the rounds via some rando class they have and see what we get
    rounds = all_rounds.find_elements(By.CLASS_NAME, 'shadow-sm')

    # this should be 11 as of 10/17
    assert len(rounds) == round_count
    
    # make some emptiness
    rounds_data = {}

    # iterate through each element to find some info on each round
    for elem in rounds:
        # check if this round is the current round - if so, skip it!
        if 'current' in elem.get_attribute('class'):
            continue

        # get the id, used to click the button into the round later
        round_id = elem.get_attribute('id')

        # get the title from the h5
        round_title = elem.find_element(By.CSS_SELECTOR, 'h5').text
        
        # programmatically get the round number
        round_num = elem.find_element(By.CSS_SELECTOR, 'strong.d-block.mb-1').text

        # make it nicer
        round_num = round_num.replace(' ', '_').lower()

        # and add it all to the dictionary!
        rounds_data[round_id] = round_num

        # now we can loop through each week using the ids from above
    for round_id, round_num in rounds_data.items():
        # print it
        print(round_num)

        # get the button that would take us into the results of this week
        round_button = getBy(driver, 'xpath', f"//a[contains(@href, '{round_id}')]")

        # scroll down so we can see this button
        driver.execute_script('arguments[0].scrollIntoView();', round_button)

        # wait a few seconds while we scroll...
        time.sleep(rand_wait())

        # ...and click!
        round_button.click()

        # i want to wait here to make sure the entire page loaded
        time.sleep(rand_wait(bot = 7, top = 10))

        # now we can just save out the source of this page as some html to use later in BeautifulSoup
        with open(f"./tmp/{round_num}.html", 'w') as f:
            f.write(driver.page_source)

        # go back a page and do it all again
        driver.back()
    
    # daddy says to always wait
    time.sleep(rand_wait())

    return