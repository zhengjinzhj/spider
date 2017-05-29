# -*- coding:utf-8 -*-

from selenium import webdriver
import time
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-data-dir=C:\Users\zheng\AppData\Local\Google\Chrome\User Data')
chrome = webdriver.Chrome(chrome_options=chrome_options)


def get_page_url():
    url_title_dict = {}
    # 226-IMiss, 225-MiStar, 223-MyGirl, 227-MFStar, 228-FEILIN
    main_url = 'http://www.ftoow.com/thread.php?fid-225-page-'
    for i in (1, 2):
        index_page_url = main_url + str(i) + '.html'
        chrome.get(index_page_url)
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        if i == 1:
            contents = soup.find('tr', class_='tr4').find_next_siblings('tr')  # siblings(trs after first tr)
        else:
            contents = soup.find('table', class_='z').find_all('tr')  # children(trs under table)
        for content in contents:  # a content is a tr
            item = content.find('a', class_='subject_t')  # a tag(that has class key) under tr tag
            link = 'http://www.ftoow.com/' + item['href'].strip()
            name = item.string.strip()
            # find the albums before particular one (may downloaded already last time)
            if 'Vol.158' in name:
                break
            url_title_dict.setdefault(link, name)
    return url_title_dict


def from_page_link(url, name):
    # url is the album page url, something like this: http://www.ftoow.com/read.php?tid-32350.html
    chrome.get(url)

    # use find_elementS to judge the element exists or not
    download_button = chrome.find_elements_by_class_name('down')
    if len(download_button) != 0:
        get_password = chrome.find_elements_by_xpath('//a[@class="down"]/ancestor::span[2]/following-sibling::span')
        if len(get_password) != 0:
            password = get_password[0].text.strip()
        else:
            pw_soup = BeautifulSoup(chrome.page_source, 'html.parser')
            password = pw_soup.find('a', class_='down').nextSibling[-5:]

        # target="_blank" means open the link in a new tab, remove it to let the link open within the tab
        js = 'document.getElementsByClassName("down")[0].target="";'
        chrome.execute_script(js)

        chrome.find_element_by_class_name('down').click()
        chrome.find_element_by_xpath('//*[@id="accessCode"]').send_keys(password)
        chrome.find_element_by_xpath('//*[@id="submitBtn"]/a').click()
        # 隐形等待是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。
        # 隐性等待对整个driver的周期都起作用，所以只要设置一次即可。
        # chrome.implicitly_wait(5)
        time.sleep(3)
        chrome.find_element_by_class_name('g-button-right').click()
        # locator = (By.CLASS_NAME, 'g-button-right')
        # WebDriverWait(chrome, 3).until(ec.presence_of_element_located(locator))
        time.sleep(3)
        chrome.find_element_by_xpath('//*[@id="fileTreeDialog"]/div[4]/a[2]/span').click()
        time.sleep(2)
        print name + ' is saved.'
    else:
        print name + ' is not free!!!'


for k, v in get_page_url().items():
    # from_page_link(k, v)
    print k, v
chrome.quit()




