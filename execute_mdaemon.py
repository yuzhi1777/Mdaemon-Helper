from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import csv
import time
import pathlib
from config import admin_user, admin_passwd


def get_list():
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_user(**row)
            #test_ordered_dict(**row)

def main():
    driver.find_element_by_id('username').send_keys(admin_user)
    driver.find_element_by_id('password').send_keys(admin_passwd)
    driver.find_element_by_id('Logon').click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'AccountsLink'))
        )
        element.click()
        #开始创建账号
        get_list()
    finally:
        driver.quit()
def create_user(**args):
    # 新建账号
    driver.find_element_by_id('NewButton').click()
    #捕捉新建账号iframe进行操作
    driver.switch_to_default_content()
    print(args)
    driver.switch_to_frame('dialog:useredit_account.wdm')
    #FullName
    driver.find_element_by_id('FullName').send_keys(args['FullName'])
    #Mailbox
    element = driver.find_element_by_id('Mailbox')
    element.click()
    for i in range(10):
        element.send_keys(Keys.BACKSPACE)
    element.send_keys(args['Mailbox'])
    #Password
    driver.find_element_by_id('Password').send_keys(args['Password'])
    #Password2
    driver.find_element_by_id('Password2').send_keys(args['Password'])
    #SaveButton
    driver.find_element_by_id('SaveButton').click()
    time.sleep(2)
    #用户创建成果Alert
    driver.switch_to_alert().accept()
    #MAFolderGroups
    driver.find_element_by_id('MAFolderGroups').click()
    #//*[@id="AvailableGroups"]/option[2]
    driver.find_element_by_xpath('//*[@id="AvailableGroups"]/option[28]').click()
    #Left  name
    driver.find_element_by_name('Left').click()
    #SaveButton
    driver.find_element_by_id('SaveButton').click()
    time.sleep(2)
    #MAAdminNotes
    driver.find_element_by_id('MAAdminNotes').click()
    #Content
    driver.find_element_by_name('Content').send_keys(args['IDcard'])
    #SaveButton
    driver.find_element_by_id('SaveButton').click()
    time.sleep(2)
    #关闭新建账号页面
    driver.switch_to_default_content()
    driver.find_element_by_xpath('//*[@id="theBody"]/div[5]/div/a[2]').click()

if __name__ == '__main__':
    p = pathlib.Path('.')
    file_path = p / 'list.csv'
    fieldnames = ['Mailbox', 'oapassword', 'FullName', 'Mailboxadd', 'Password', 'IDcard']

    driver = webdriver.Chrome('./chromedriver')
    driver.implicitly_wait(10)
    driver.get("https://mail.juneyaoair.com:1001/")
    assert "MDaemon" in driver.title
    main()
