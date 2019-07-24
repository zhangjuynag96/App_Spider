from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import pymongo
import re
import time
from selenium.common.exceptions import NoSuchElementException


#Appium服务设置
server = 'http://localhost:4723/wd/hub'
#虚拟机设置
desired_caps = {
  "platformName": "Android",
  "deviceName": "SM_A7009",
  "appPackage": "com.tencent.mm",
  "appActivity": ".ui.LauncherUI"
}
#执行最长等待时间
TIMEOUT = 300
#Mongodb设置
MONGO_URL = 'localhost'
MONGO_DB = 'wechatcircle'
MONGO_COLLECTION = 'activity'
#账户密码设置
ACCOUNT = '17755903983'
PASSWORD = 'o00oo0o230'
#滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 1100
# 滑动间隔
SCROLL_SLEEP_TIME = 3

class Processor():
    def date(self,datetime):
        '''
        处理时间
        :param datetime: 原始时间
        :return: 处理后的时间
        '''
        if re.match('\d+分钟前',datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', datetime):
            hour = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天', datetime):
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d+天前', datetime):
            day = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(day) * 60 * 60 * 24))
        return datetime

class WechatCircle():
    def __init__(self):
        '''
        初始驱动配置
        '''
        self.desired_caps = desired_caps
        self.driver = webdriver.Remote(server, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        self.processor = Processor()

    def login(self):
        '''
        模拟微信登录
        '''
        #登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/e80')))
        login.click()
        #输入账户
        account = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/l3')))
        account.set_text(ACCOUNT)
        #提交账户信息，进入下一步
        next = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/ay8')))
        next.click()
        #输入密码
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/l3')))
        password.set_text(PASSWORD)
        #提交密码信息，进入下一步
        next.click()
        #解决验证通讯录问题
        phone_list = self.wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/azz')))
        phone_list.click()

    def enter(self):
        '''
        模拟进入朋友圈
        '''
        #选择选项卡
        self.driver.tap([(637, 1785), (713, 1861)], 500)  # positioning element nodes by coordinates
        #进入朋友圈
        friend_circle = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/l5')))
        friend_circle.click()

    def crawl(self):
        '''
        爬取朋友圈内容
        :return: 朋友圈信息
        '''
        while True:
            # 上划
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@resource-id="com.tencent.mm:id/eii"]//android.widget.FrameLayout')))
            #遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/b6e').get_attribute('text')
                    # 正文
                    content = item.find_element_by_id('com.tencent.mm:id/en0').get_attribute('text')
                    # 日期
                    date = item.find_element_by_id('com.tencent.mm:id/ehz').get_attribute('text')
                    # 处理日期
                    date = self.processor.date(date)
                    print(nickname, content, date)
                    data = {
                        'nickname':nickname,
                        'content':content,
                        'date':date
                    }
                    # 插入MongoDB
                    self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                    time.sleep(SCROLL_SLEEP_TIME)

                except NoSuchElementException:
                    pass

    def main(self):
        #登录
        self.login()
        #进入朋友圈
        self.enter()
        time.sleep(20)
        #爬取
        self.crawl()

if __name__ == '__main__':
    run = WechatCircle()
    run.main()