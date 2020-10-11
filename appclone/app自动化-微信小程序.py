#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Author: xiaojian
#Time: 2018/11/19 15:29

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy as MB

#引入appium包
from appium import webdriver
import time
import os

#启动appium时，需要指定chromedriver.exe的目录。使用appium默认目录下的会报错。
#在切换到小程序webview时，会去匹配chrome内核的39的驱动。在切换完成之后，在打印所有的窗口时，会使用x5内核的版本。
#所以指定一个非默认目录下面的chromedriver.exe(X5内核对应的版本)，此问题就不会出现 。
#在appium server上设置chromedriver的路径：D:\ChromeDrivers\chromedriver.exe
desired_caps = {}
#支持X5内核应用自动化配置
desired_caps["recreateChromeDriverSessions"] = True
#android 4.4以下的版本通过Selendroid来切换到webview
desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "5.1"
desired_caps["deviceName"] = "Android Emulator"
desired_caps["appPackage"] = "com.tencent.mm"
desired_caps["appActivity"] = "com.tencent.mm.ui.LauncherUI"
desired_caps["noReset"] = True

# ChromeOptions使用来定制启动选项，因为在appium中切换context识别webview的时候,
# 把com.tencent.mm:toolsmp的webview识别成com.tencent.mm的webview.
# 所以为了避免这个问题，加上androidProcess: com.tencent.mm:toolsm
# options = wb.ChromeOptions()
# options.add_experimental_option("androidProcess","com.tencent.mm:toolsmp")
desired_caps["chromeOptions"] = {"androidProcess":"com.tencent.mm:toolsmp"}
desired_caps["browserName"] = ""

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)

#
time.sleep(5)
#点击发现
driver.find_element_by_android_uiautomator('new UiSelector().text(\"发现\")').click()
#点击发现里面搜一搜
driver.find_element_by_android_uiautomator('new UiSelector().text(\"搜一搜\")').click()
#等待搜索框出现
WebDriverWait(driver,20).until(EC.visibility_of_element_located((MB.ID,"com.tencent.mm:id/jd")))
#点击搜索框
driver.find_element_by_id("com.tencent.mm:id/jd").click()
#driver.find_element_by_id("com.tencent.mm:id/jd").send_keys("柠檬班软件测试")
time.sleep(5)
# #点击历史记录中的柠檬班软件测试（采用adb命令坐标点击的方式)
os.system("adb shell input tap 281 205")
# #点击柠檬班软件测试小程序
time.sleep(5)
os.system("adb shell input tap 364 470")
# #等待小程序加载完成
time.sleep(14)
#获取所有的上下文
cons = driver.contexts
print("当前所有的上下文为：",cons)

#切换到小程序webview
driver.switch_to.context("WEBVIEW_com.tencent.mm:toolsmp")
#打印当前所有的窗口
hs = driver.window_handles
print("当前所有的窗口为：",hs)
#print("当前所在的窗口为：",driver.current_window_handle)
#需要找到哪一个窗口有柠檬班信息的窗口，然后再在其下找元素操作。
#遍历所有的handles，找到当前页面所在的handle：如果pageSource有包含你想要的元素，就是所要找的handle
#小程序的页面来回切换也需要：遍历所有的handles，切换到元素所在的handle
for handle in hs:
    driver.switch_to.window(handle)
    print("切换到窗口：",handle)
    time.sleep(3)
    #print(driver.page_source)
    if driver.page_source.find("柠檬班") != -1:
        break

#点击老师
WebDriverWait(driver,20).until(EC.visibility_of_element_located((MB.XPATH,"//*[@id=\"js-tab-bar\"]/li[3]"))).click()
WebDriverWait(driver,20).until(EC.presence_of_element_located((MB.XPATH,"//em[text()='歪歪']")))
time.sleep(0.5)
#找到歪歪老师
ele = driver.find_element_by_xpath("//em[text()='歪歪']")
#拖动到可见区域
driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);",ele)





