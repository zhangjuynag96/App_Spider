from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import pymongo
import re
import time
from selenium.common.exceptions import NoSuchElementException

# Appium服务设置
server = 'http://localhost:4723/wd/hub'
# 虚拟机设置
desired_caps = {
  "platformName": "Android",
  "deviceName": "SM_A7009",
  "appPackage": "com.jingdong.app.mall",
  "appActivity": "com.jingdong.app.mall.main.MainActivity",
  "platformVersion": "5.0.2"
}
# 执行最长等待时间
TIMEOUT = 300
# 物品关键词
KEYWORD = 'iphone'
# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 1300
# 滑动间隔
SCROLL_SLEEP_TIME = 1

class Action(object):
    def __init__(self):
        #驱动配置
        self.desired_caps = desired_caps
        self.driver = webdriver.Remote(server, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def comments(self):
        #进入搜索界面
        tips = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/brt')))
        tips.click()
        start = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/c7y')))
        start.click()
        time.sleep(10)
        close = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/nh')))
        close.click()
        self.driver.tap([(35, 203), (1046, 292)], 500)
        box = self.wait.until(EC.presence_of_element_located((By.ID,'com.jd.lib.search:id/a0m')))
        box.set_text(KEYWORD)
        button = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/ay1')))
        button.click()
        view = self.wait.until(EC.presence_of_element_located((By.ID,'com.jd.lib.search:id/a06')))
        view.click()
        time.sleep(10)
        self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
        product = self.wait.until(EC.presence_of_element_located((By.ID,'com.jd.lib.productdetail:id/ad4')))
        product.click()
        comments = self.wait.until(EC.presence_of_element_located((By.ID,'com.jd.lib.productdetail:id/ad5')))
        comments.click()

    def scroll(self):
        while True:
            # 模拟拖动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            time.sleep(SCROLL_SLEEP_TIME)

    def main(self):
        self.comments()
        self.scroll()

if __name__ == '__main__':
    action = Action()
    action.main()