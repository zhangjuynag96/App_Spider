from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import time

server = 'http://localhost:4723/wd/hub'

desired_caps = {
  "platformName": "Android",
  "deviceName": "SM_A7009",
  "appPackage": "com.tencent.mm",
  "appActivity": ".ui.LauncherUI"
}

driver = webdriver.Remote(server,desired_caps)
wait = WebDriverWait(driver,30)
login = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/e80')))
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/l3')))
phone.set_text('xxxxxxxxxxxxx')
phone_login = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/ay8')))
phone_login.click()
password = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/l3')))
password.set_text('xxxxxxxxxx')
phone_login.click()
celebary = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/azz')))
celebary.click()
# discover = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/azz')))
# discover.click()
time.sleep(20)
driver.tap([(637,1785),(713,1861)],500)  #positioning element nodes by coordinates
friend_circle = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/l5')))
friend_circle.click()
action = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/kj')))
TouchAction(driver).long_press(action).perform()
time.sleep(3)
tip = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/cra')))
tip.click()
article = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/csj')))
article.set_text('its a appium spider test')
article_send = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/ki')))
article_send.click()

#-------------------------------------------------------------------------------------------------
#浮动评论问题
# comment = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/eho')))
# comment.click()
# comment.click()
# driver.tap([(670,1125),(929,1233)],500)
# comment_article = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/eif')))
# comment_article.set_text('test1')
# comment_article_send = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/eih')))
# comment_article_send.click()

delete = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/ei5')))
delete.click()
delete_sure = wait.until(EC.presence_of_element_located((By.ID,'com.tencent.mm:id/b00')))
delete_sure.click()
