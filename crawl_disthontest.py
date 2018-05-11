# coding=utf-8
'''
Created on 2018年5月11日

@author: DA
'''
import time
import csv
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

driver = webdriver.Firefox()
driver.implicitly_wait(2)  # 隐形等待
driver.maximize_window()  # 全屏最大化
driver.get("""
        https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA&rsv
   ...: _pq=9e72ec370004fe8b&rsv_t=1454OS4vtYDZyHz5QxDsra%2BT9%2BkOtkzxbxw5Md18MJ5oYthv4ywp3pF6K08&rqlang=cn&rsv_enter=
   ...: 1&rsv_sug3=9&rsv_sug1=8&rsv_sug7=100""")  # 初始网页
# 文件存储路径
csvpath = "C:/python books/python_practice/src/web_crawler/crwaler_test/national_dishontest/nations_dishonest.csv"
csvfile = open(csvpath, 'a+', newline='', encoding='gbk')
writer = csv.writer(csvfile, delimiter='~')
keys = ['身份证','姓名','执行法院','省份','案号','生效法律文书确定的义务','被执行人的履行情况',
        '失信被执行人行为具体情形','发布时间']
writer.writerow(keys)

ids_list = []
names_list = []

for i in range(2):
    """调整爬取页面次数"""
    ids = driver.find_elements_by_xpath("//span[@class='op_trust_fl op_trust_papers']")
    names = driver.find_elements_by_xpath("//span[@class='op_trust_name']")

    for i in range(len(ids)):
        id = ids[i].text
        if len(id) == 19:
            """仅爬取个人信息"""
            id = id[:14] + id[15:]  # 去除多余的*
            name = names[i].text
        
            actions = ActionChains(driver)
            actions.click(ids[i]).perform()
            time.sleep(3)
        
            if id not in ids_list and name not in names_list:
                """仅保存没有重复的记录"""
                ids_list.append(id)
                names_list.append(name)
                
                court = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[1]/td[2]")[i].text
                province = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[2]/td[2]")[i].text
                no = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[3]/td[2]")[i].text
                info = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[4]/td[2]")[i].text
                action = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[5]/td[2]")[i].text
                law = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[6]/td[2]")[i].text
                date = driver.find_elements_by_xpath("//div[@class='op_trust_info']/table/tbody/tr[7]/td[2]")[i].text
                
                writer.writerow([id, name, court, province, no, info, action, law, date])
    
    # 移动到下一页
    nextfield = driver.find_elements_by_xpath("//div[@class='op_trust_page c-gap-bottom']/p/span[last()]")[0]
    actions = ActionChains(driver)
    actions.click(nextfield).perform()
    time.sleep(4)

driver.close()  # 关闭浏览器
