# coding=utf-8
'''
Created on 2018年5月15日

@author: DA
'''
import time
import random
import pymysql
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

ids_list = []
names_list = []

conn = pymysql.connect(host='127.0.0.1', port=3306, user='XXXX', password='XXXX', db='XXXX', charset='utf8') # 连接数据库
cur = conn.cursor()
cur.execute('USE XXXX;') # 在运行程序前，本地创建好相应数据库
cur.execute("""
CREATE TABLE IF NOT EXISTS `national_dishonest` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '编号',
    `id_no` varchar(20) NOT NULL COMMENT '身份证',
  `name` varchar(50) NOT NULL COMMENT '姓名',
  `court` varchar(50) DEFAULT NULL COMMENT '执行法院',
  `province` varchar(20) DEFAULT NULL COMMENT '省份',
  `no` varchar(50) DEFAULT NULL COMMENT '案号',
  `info` varchar(5000) DEFAULT NULL COMMENT '生效法律文书确定的义务',
  `action` varchar(50) DEFAULT NULL COMMENT '被执行人的履行情况',
  `law` varchar(50) DEFAULT NULL COMMENT '失信被执行人行为具体情形',
  `date` varchar(20) DEFAULT NULL COMMENT '发布时间',
  `update_time` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  KEY `id` (`id`),
    UNIQUE KEY `unique_key` (`id_no`, `name`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='全国个人失信人名单';
""")

for i in range(2):
    """调整爬取页面次数"""
    ids = driver.find_elements_by_xpath("//span[@class='op_trust_fl op_trust_papers']")
    names = driver.find_elements_by_xpath("//span[@class='op_trust_name']")

    for i in range(len(ids)):
        id = ids[i].text
        if len(id) == 19 and id[0] != '9' and id[:11].isdigit() and id[-4:-1].isdigit() and \
        (id[-1] == 'x' or id[-1] == 'X' or id[-1].isdigit()):
            """仅爬取个人信息"""
            id = id[:14] + id[15:]  # 去除多余的*
            name = names[i].text
        
            actions = ActionChains(driver)
            actions.click(ids[i]).perform()
            time.sleep(random.randint(3,5))
        
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
                # mysql中插入数据
                try:
                    cur.execute("INSERT INTO national_dishonest (\
                    id_no, name, court, province, no, info, action, law, date) VALUES(\
                    %s, %s, %s, %s, %s, %s, %s, %s, %s);", \
                    (id, name, court, province, no, info, action, law, date)
                    )  
                    cur.connection.commit()
                except Exception as e:
                    print(e)
                  
    # 移动到下一页
    nextfield = driver.find_elements_by_xpath("//div[@class='op_trust_page c-gap-bottom']/p/span[last()]")[0]
    actions = ActionChains(driver)
    actions.click(nextfield).perform()
    time.sleep(random.randint(4,6))

cur.close()
conn.close()  # 关闭数据库
driver.close()  # 关闭浏览器

