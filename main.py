# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
import json
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import codecs
import os


import pandas as pd

#TODO: Modify this
DATA_PATH = '/path/to/dread-scraper/data/'

# Links of interest
dread_main = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion'
dread_main_w_pagination = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/?p={}'.format('PAGE')

dread_search = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/search/?q={}&sort=best&fuzziness=auto'.format('SEARCH_TERM')
dread_search_w_pagination = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/search/?p={}&sort=best&q={}&fuzziness=auto'.format('PAGE', 'SEARCH_TERM')


def get_post_links_through_search(search_term, start_page):
    # E.g., search_term = 'scammer'
    #       start_page = '1'
    print('{} - Begin saving links from Dread search.'.format(datetime.now().strftime("%H:%M:%S")))
    print('SEARCH TERM: {}'.format(search_term))
    print('STARTING PAGE: {}'.format(start_page))

    # Create the folder where we are going to save the scrapes
    scrapes_savepath = DATA_PATH + 'search_term={}/'.format(search_term)
    if not os.path.isdir(scrapes_savepath):
        os.mkdir(scrapes_savepath)
    else:
        print('Error: We may have already scraped this search term, double check save path...')
        return -1

    print('Saving results to {}'.format(scrapes_savepath))

    url_list = []
    current_page = int(start_page)
    page_ct =0
    ##### SCRAPE SEARCH RESULTS AND GET URLs
    while True:
        now = datetime.now()
        page_ct += 1
        if random.randint(5,12) == page_ct:
            print('Breaking within pages to not get rate limited.')
            page_ct = 0
            time.sleep(random.uniform(30,120))

        dread_search_w_pagination = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/search/?p={}&sort=best&q={}&fuzziness=auto'\
        .format(current_page, search_term)
        print('{} - Loading PAGE {}....'.format(now.strftime("%H:%M:%S"), current_page))

        driver.get(dread_search_w_pagination)
        elements = driver.find_elements_by_class_name("title")
        for e in elements:
            try:
                post_url = e.get_attribute('href')
                url_list.append(post_url)
                print('Saved: {}'.format(post_url))
            except Exception as e:
                print(e)

        print('Saving progress to {}/urls-500.txt'.format(scrapes_savepath))
        with open(scrapes_savepath + 'urls-500.txt'.format(search_term), 'w') as fw:
            json.dump(url_list, fw)

        with open(scrapes_savepath + 'PAGE', 'w') as fw:
            json.dump(current_page, fw)

        current_page = current_page + 1

        if current_page == 499:
            break
        print('{} - Finished page {}, continuing to page {}'.format(now.strftime("%H:%M:%S"), current_page, current_page + 1))
        time.sleep(random.uniform(9,15))

    return url_list


def get_post_links_through_main(start_page):
    # E.g., start_page = '1'
    print('{} - Begin saving links from Dread Homepage.'.format(datetime.now().strftime("%H:%M:%S")))
    '''
    Create the folder where we are going to save the scrapes
    Because we are scraping based on the main page, we save the time date when we started scraping instead
    As time passes, the content of each page will change
    '''
    scrapes_savepath = DATA_PATH + 'homepage_scrape_date={}/'.format(datetime.now().strftime("%d_%m_%y"))
    if not os.path.isdir(scrapes_savepath):
        os.mkdir(scrapes_savepath)
    else:
        print('Error: We may have already started scraping today, double check the contents in the savepath...')
        return -1

    url_list = []
    current_page = int(start_page)
    page_ct = 0
    ##### SCRAPE PAGES AND GET URLs
    while True:
     now = datetime.now()
     page_ct += 1
     # We add a random sleep interval every couple of pages to prevent getting rate limited.
     if random.randint(5,12) % page_ct == 0:
         print('Breaking within pages to not get rate limited.')
         page_ct = 0
         time.sleep(random.uniform(30,120))

     dread_main_w_pagination = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/?p={}'\
     .format(current_page)
     print('{} - Loading PAGE {}....'.format(now.strftime("%H:%M:%S"), current_page))

     driver.get(dread_main_w_pagination)
     elements = driver.find_elements_by_class_name("title")
     for e in elements:
         try:
             post_url = e.get_attribute('href')
             url_list.append(post_url)
             print('Saved: {}'.format(post_url))
         except Exception as e:
             print(e)

     print('Saving progress to {}/urls-500.txt'.format(scrapes_savepath))
     with open(scrapes_savepath + 'urls-500.txt', 'w') as fw:
         json.dump(url_list, fw)

     with open(scrapes_savepath + 'PAGE', 'w') as fw:
         json.dump(current_page, fw)

     current_page = current_page + 1

     if current_page == 499:
         break
     print('{} - Finished page {}, continuing to page {}'.format(now.strftime("%H:%M:%S"), current_page, current_page + 1))
     time.sleep(random.uniform(9,15))

    return url_list

def get_source_pages_from_list(save_path, url_list_filepath):
    #E.g., savepath='/path/to/search_term=scam/scrapes/'
    #      url_list_filepath = '/path/to/search_term=scam/urls-500.txt
    print('{} - Going through pages in {} to save source'.format(datetime.now().strftime("%H:%M:%S"), url_list_filepath))

    # Filepath to a list of urls in the following format: ['url_1', 'url_2', ..., 'url_3']
    # Alternatively, you can pass directly a list of links
    url_list = None
    with open(url_list_filepath, 'r') as fr:
        url_list = json.load(fr)

    for i, url in enumerate(url_list):
        print('Current index: {}'.format(i))
        print('{} - Working on: {}'.format(datetime.now().strftime("%H:%M:%S"), url))
        driver.get(url)

        #Random sleep after we visit a page
        time.sleep(random.uniform(45,120))
        post_folder = url.split('/')[-1]

        # If the folder already exists, we assume we have scraped it.
        if os.path.isdir(save_path + post_folder):
            continue
        else:
        # Else, we create the folder and save the .html
            os.mkdir(save_path + post_folder)
            f = codecs.open(save_path + post_folder + '/post.html', 'w', 'utf-8')
            h = driver.page_source
            f.write(h)
            print('Source saved!')

def navigate_to_main():
    print('{} - Loading MAIN page...'.format(datetime.now().strftime("%H:%M:%S")))
    driver.get(dread_main)

    print('Saving cookies (if any)...')
    ch = driver.get_cookies()
    for c in ch:
        driver.add_cookie(c)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #binary = FirefoxBinary('/Applications/Tor Browser.app/Contents/MacOS/firefox')
    firefox_options = webdriver.FirefoxOptions()
    
    #TODO: Modify this to point to the firefox binary
    firefox_options.binary_location = '/Applications/Tor Browser.app/Contents/MacOS/firefox'
    driver = webdriver.Firefox(options=firefox_options)

    print('Sleeping for 15 on startup, waiting for TOR connection...')
    time.sleep(15)
    driver.get('http://google.com')

