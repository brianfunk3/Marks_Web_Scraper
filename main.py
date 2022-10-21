from utils import buildHeadless
from scraper import login, pull_data
from parser import parse_html

import sys
import getopt

def main(argv):
    # get the user inputs via command line, if any
    try:
        opts, args = getopt.getopt(argv, 'ru:p:')
    except getopt.GetoptError:
        print('you dingdong, you used it wrong')
        sys.exit(2)

    refresh_data = False
    for arg, val in opts:
        if arg == '-r':
            refresh_data = True

    if refresh_data:
        # build our headless driver
        driver = buildHeadless()

        # attempt to pull in credentials
        # TODO: allow passing these in via command line
        with open('credentials.txt', 'r') as f:
            email = f.readline().strip()
            password = f.readline().strip()

        # log in to the website with spotify account
        login(driver, email, password)

        # now pull the data!
        pull_data(driver)        

        # bye
        driver.close()


    # now we can parse the data
    parse_html()

# make sure we pass in those command-line arguments!
if __name__ == '__main__':
    main(sys.argv[1:])