import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import json
import os
from utils import getConfig, createEmail, createStr


def register(url, email, password,driver):
    """注册网站

    Args:
        url: 注册网址
        email: 注册邮箱
        password: 注册密码
        driver: 浏览器实例
    """
    driver.get(url)

    emailInput = driver.find_element_by_xpath(
        '//*[@id="main-container"]/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]/input')
    passwordInput = driver.find_element_by_xpath(
        '//*[@id="main-container"]/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/input')
    rePasswordInput = driver.find_element_by_xpath(
        '//*[@id="main-container"]/div[2]/div/div[2]/div/div[1]/div/div/div/div[3]/input')
    btn = driver.find_element_by_xpath(
        '//*[@id="main-container"]/div[2]/div/div[2]/div/div[1]/div/div/div/div[5]/button')

    emailInput.send_keys(email)
    passwordInput.send_keys(password)
    rePasswordInput.send_keys(password)
    try:
        btn.click()

        # 避免第一次点击未出现验证码
        time.sleep(3)
        btn.click()
        print('点击注册...')
    except:
        pass


def check_element_exists(driver):
    """校验当前注册状态

    Args:
        driver: 浏览器实例
    
    Returns:
        布尔值
        example:
            True:  注册成功
            False: 注册失败
    """
    print('************')

    for i in range(retry):
        try:
            # 获取到说明登录成功，反之报错
            driver.find_elements_by_xpath(
                '//*[@id="page-header"]/div/div[2]')[0]
            
            print('************')
            print('注册成功')
            return True
        except:
            print(f'正在注册中 请稍后「 {i + 1} 」')
            time.sleep(3)

    return False


def login(url, email, password):
    """校验当前注册状态

    Args:
        url: 登录网址
        email: 登录邮箱
        password: 登录密码
    
    Returns:
        TOKEN
        example:
            dfc5141d3dhbjwaqdheui16ad395c9782352
    """

    data = {
        'email': email,
        'password': password
    }

    try:
        res = requests.post(url, data=data).text
        res = json.loads(res)
        return res['data']['token']
    except:
        print('token获取错误')


def save(email, password, url):
    with open(savePath + 'user.txt', 'w') as f:
        f.write(f"{email}\t\t{password}\n{url}\n")
        print('保存成功: ' + savePath + 'user.txt')


def createUrl(webUrl, token, flag):
    # TODO(): 后续可能修改 
    if flag == 0:
        webUrl = 'http://rss.msclm.net'

    url = f"https://sub.xeton.dev/sub?target=surfboard&url={webUrl}api/v1/client/subscribe?token={token}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini"
    return url


def run(i):
    """启动程序

    Args:
        i: 选择网站
    
    Returns:
        失败or订阅链接
        example:
            https://sub.xeton.dev/sub
            ?target=surfboard
            &url=https://msclm.xyz/api/v1/client/subscribe?token=213213
            &insert=false
            &config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini
    """
    driver = getDriver()
    email = createEmail(1)
    password = createStr(10)

    if driver == None:
        print('实例启动失败')
        return

    try:
        register(urlList[i]['registerUrl'], email, password, driver)

        if check_element_exists(driver):
            token = login(urlList[i]['loginUrl'], email, password)
            webUrl = urlList[i]['registerUrl'].split('#')[0]

            os.popen('pkill Google')
            save(email, password)
            
            return createUrl(webUrl, token)
        else:
            os.popen('pkill Google')
            return '获取失败'
    except IndexError:
        return "该选项不存在"


def getDriver():
    # print(chromePath)
    if webdriver.common.utils.is_connectable(port) == False:
        command = f'{chromePath} --load-extension="./yesCaptcha/" --remote-debugging-port={port} --user-data-dir="./config/chrome/"'
        os.popen(command)


    options = Options()
    options.add_experimental_option(f"debuggerAddress", f"{ip}:{port}")
    driver = webdriver.Chrome(options=options)
    return driver


if __name__  in ['__main__','vpn']:

    try:
        vpnConfig = getConfig('vpn')
        chromePath = vpnConfig['chromePath']
        ip = vpnConfig['ip']
        port = vpnConfig['port']
        urlList = vpnConfig['url_list']
        retry = vpnConfig['retry']
        savePath = vpnConfig['savePath']
    except:
        print('配置获取失败')



    
    