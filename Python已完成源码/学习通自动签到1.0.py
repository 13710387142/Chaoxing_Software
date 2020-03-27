import requests
import json
import time
from selenium import webdriver # 从selenium导入webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
print("欢迎使用自动学习通自动签到软件，如有多个课程请多开")
username=input("请输入手机号：") #输入框输入
password=input("请输入密码：") #输入框输入

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
userElement.send_keys(username) #输入框输入
pwdButton.send_keys(password) #输入框输入
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
#print (cookie_text)
# 关闭浏览器
driver.close()

#软件开始
#cookie_user=input("输入Cookie启动程序:")
cookie_user =cookie_text
#填入Cookie
headers={
 "Cookie": cookie_user,
 "User-Agent": ""
}
#填入uid
uid=""
coursedata=[]
activeList=[]
course_index=0
speed=10
status=0
status2=0
activates=[]
def backclazzdata():
 global coursedata
 url="http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
 res=requests.get(url,headers=headers)
 cdata=json.loads(res.text)
 if(cdata['result']!=1):
  print("请补充Cookie否则课程列表获取失败")
  return 0
 for item in cdata['channelList']:
  if("course" not in item['content']):
   continue
  pushdata={}
  pushdata['courseid']=item['content']['course']['data'][0]['id']
  pushdata['name']=item['content']['course']['data'][0]['name']
  pushdata['imageurl']=item['content']['course']['data'][0]['imageurl']
  pushdata['classid']=item['content']['id']
  coursedata.append(pushdata)
 print("获取成功") 
 #print(coursedata) 
 printdata()
 
def printdata():
 global course_index,speed
 index=1
 for item in coursedata:
  print(str(index)+".课程名称:"+item['name'])
  index+=1
 course_index=int(input("请输入监控课程监控课程序号："))-1
 print("监控课程设定完成")
 speed=int(input("输入监控频率(以秒为单位):")) #频率是监控的速度，一格10秒，适中选择就好
 print("监控频率设置完毕")
 res=input("输入start启动监控:")
 if(res=="start"):
  startsign()
 else:
  printdata 
 
def taskactivelist(courseId,classId):
 global activeList
 url="https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId="+str(courseId)+"&classId="+str(classId)+"&uid="+uid
 res=requests.get(url,headers=headers)
 data=json.loads(res.text)
 activeList=data['activeList']
 #print(activeList)
 for item in activeList:
  if("nameTwo" not in item):
   continue
  if(item['activeType']==2 and item['status']==1):
   signurl=item['url']
   aid = getvar(signurl)
   if(aid not in activates):
    print("【签到】查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s"%(item['nameOne'],item['nameTwo'],item['nameFour'],aid))
    sign(aid,uid) 
 
def getvar(url):
 var1 = url.split("&")
 for var in var1:
  var2 = var.split("=")
  if(var2[0]=="activePrimaryId"):
   return var2[1]
 return "ccc" 
 
def sign(aid,uid):
 global status,activates
 url="https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+aid+"&uid="+uid+"&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
 res=requests.get(url,headers=headers)
 if(res.text=="success"):
  print("用户:"+uid+" 签到成功！")
  activates.append(aid)
  status=2
 else:
  print("签到失败") 
  activates.append(aid) 
 
def startsign():
 global status,status2
 status=1
 status2=1
 ind=1
 print("监控启动 监控课程为:%s 监控频率为:%s秒一次"%(coursedata[course_index]['name'],str(speed)))
 
 while(status!=0 and status2!=0):
  ind+=1
  taskactivelist(coursedata[course_index]['courseid'],coursedata[course_index]['classid'])
  time.sleep(speed)
  if(status==1):
   print(str(ind)+" [签到]监控运行中，未查询到签到活动")
  elif(status==2):
   print(str(ind)+" [新签到]监控运行中，未查询到签到活动")   
 print("任务结束")
 printdata()
 
backclazzdata()
