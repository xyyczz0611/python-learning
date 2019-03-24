import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
import pandas as pd
import sys



Titles = []
Contents = []
pages_selected = []

driver = webdriver.Chrome('D:\Program Files\chromedriver_win32\chromedriver.exe')
driver.get('https://www.jiqizhixin.com/dailies')
time.sleep(5)

def load():
    driver.find_element_by_xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "u-loadmore__btn", " " ))]').click()

def Download(date1, date2):
    end_month = int(date2[:2])   #去除可能存在的0
    end_day = int(date2[2:])
    start_month = int(date1[:2])  
    start_day = int(date1[2:])
    today_month = int(driver.find_element_by_css_selector('.daily-every__month').text[:-1]) #去掉月
    today_day = int(driver.find_element_by_css_selector('.daily-every__day').text)
    page_month = today_month
    page_day = today_day
    while True:
        load()
        page_month = int(driver.find_elements_by_css_selector('.daily-every__month')[-1].text[:-1])
        page_day = int(driver.find_elements_by_css_selector('.daily-every__day')[-1].text)
        time.sleep(5)
        if (page_month == start_month and page_day == start_day):
            break
    pages = driver.find_elements_by_css_selector('.daily-every.js-daily-every')
    del pages[-1]
    for page in pages[::-1]:
        index1 = page.text.find('月')
        index2 = page.text.find('\n')
        pages_selected.append(page)
        if (int(page.text[:index1])==end_month and int(page.text[index1+1:index2])==end_day):
            break
            
    for item in pages_selected:
        titles = item.find_elements_by_css_selector('.js-open-modal')
        contents = item.find_elements_by_css_selector('.daily__content')
        for title in titles:
            Titles.append(title.text)
        for content in contents:
            Contents.append(content.text)


if __name__ == '__main__':
	print('抓取中')
	date1 = sys.argv[1]
	date2 = sys.argv[2]
	Download(date1,date2)
	dic = {'title':Titles,'content':Contents}
	output = pd.DataFrame(dic)
	output.to_csv('AI daily.csv', encoding='utf_8_sig')
	print ('抓取已完成')
	driver.quit()