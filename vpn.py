import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import os
from utils import getConfig, createEmail, createStr, getHeaders


def register(url, email, password, driver):
    """注册网站

    Args:
        url: 注册网址
        email: 注册邮箱
        password: 注册密码
        driver: 浏览器实例
    """
    driver.get(url)

    inputList = driver.find_elements_by_tag_name('input')
    btn = driver.find_elements_by_tag_name('button')[0]

    emailInput = inputList[0]
    passwordInput = inputList[1]
    rePasswordInput = inputList[2]
    
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


def check_element_exists(driver, email='', password=''):
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
        if 'login' in driver.current_url:
            print('ok')
            print('login' in driver.current_url)
            print(email, password)

            inputList = driver.find_elements_by_tag_name('input')
            btn = driver.find_elements_by_tag_name('button')[0]

            inputList[0].send_keys(email)
            inputList[1].send_keys(password)
            btn.click()

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

    headers = getHeaders(url.replace('api/v1/passport/auth', '#'))
    try:
        res = session.post(url, data=data, headers=headers)
    except:
        print('登录失败')


# def save(email, password, url):
#     with open(savePath + 'user.txt', 'w') as f:
#         f.write(f"{email}\t\t{password}\n{url}\n")
#         print('保存成功: ' + savePath + 'user.txt')


def createUrl(webUrl):
    # TODO(): 后续可能修改 

    print(webUrl)
    res = session.get(webUrl).json()
    subscribe_url = res['data']['subscribe_url']

    url = f"https://sub.xeton.dev/sub?target=surfboard&url={subscribe_url}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini"
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

        if check_element_exists(driver, email, password):
            login(urlList[i]['loginUrl'], email, password)
            webUrl = urlList[i]['loginUrl'].replace('passport/auth/login', 'user/getSubscribe')

            os.popen('pkill Google')
            # save(email, password)

            return createUrl(webUrl)
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

    session = requests.Session()

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

    # https://www.wuyuandianpu.com/api/v1/user/getSubscribe
    # https://www.wuyuandianpu.com/api/v1/user/getSubscribe
    



    
    