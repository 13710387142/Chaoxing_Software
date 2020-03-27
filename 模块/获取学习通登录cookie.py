from selenium import webdriver # 从selenium导入webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 不启动界面显示- linux下命令行模式必须启用
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)  # Optional argument, if not specified will search path.
driver.get('https://passport2.chaoxing.com/login?fid=&newversion=true') # 获取页面

# 输入账号密码
userElement = driver.find_element_by_id('phone') 
pwdButton = driver.find_element_by_id('pwd') #密码输入框
subButton = driver.find_element_by_id('loginBtn') #登录按钮
userElement.send_keys("15768022010") #输入框输入
pwdButton.send_keys("wsygdsb0119.") #输入框输入
subButton.click()
time.sleep(5)
#获取cookie
cookie_items = driver.get_cookies()
cookie_str = ""
#组装cookie字符串
for item_cookie in cookie_items:
    item_str = item_cookie["name"]+"="+item_cookie["value"]+"; "
    cookie_str += item_str
#打印出来看一下
cookie_text = cookie_str[cookie_str.index("xxtenc="):]
print (cookie_text)
# 关闭浏览器
driver.close()
