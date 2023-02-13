import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import os
from .utils import getConfig, createEmail, createStr, getHeaders, save, upload, getIp


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
    print('正在登录...')
    data = {
        'email': email,
        'password': password
    }

    headers = getHeaders(url.replace('/api/v1/passport/auth/login', ""))
    try:
        res = session.post(url, data=data, headers=headers)
        print("登录成功")
        return True
    except:
        print('登录失败')
        return False


def createUrl(url):
    # TODO(): 后续可能修改 

    res = session.get(url).json()
    subscribe_url = res['data']['subscribe_url']

    url = f'https://sub.id9.cc/sub?target={mode}&new_name=true&url={subscribe_url}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini'
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
    email = createEmail()
    password = createStr(10)

    if driver == None:
        print('实例启动失败')
        return

    urls = urlList[i]
    registerUrl = urls['url'] + '/#/register'
    subscribeUrl = urls['url'] + '/api/v1/user/getSubscribe'
    loginUrl = urls['url'] + '/api/v1/passport/auth/login'
    name = urls['name']

    try:
        register(registerUrl, email, password, driver)

        if not check_element_exists(driver, email, password):
            print('获取失败')
            os.popen('pkill Google')
            return '获取失败'
        
        os.popen('pkill Google')
        flag = login(loginUrl, email, password)
        if not flag:
            return '登录失败'

        # # 启动订阅转换服务
        # os.popen('pkill subconver')
        # os.popen(f'nohup {subconverterPath} > ./log/subconverter.log 2>&1 &')
        vpnUrl = createUrl(subscribeUrl)
        flag = save(vpnUrl, urls['name'])

        if not flag:
            return vpnUrl
        
        flag2 = upload(urls['name'])
        if not flag2:
            return vpnUrl
        
        # 关闭订阅转换服务
        # os.popen('pkill subconver')
        return '上传成功'
            
    except IndexError:
        return "该选项不存在"


def getDriver():
    if webdriver.common.utils.is_connectable(port) == False:
        command = f'{chromePath} --load-extension="./yesCaptcha/" --remote-debugging-port={port} --user-data-dir="./config/chrome/"'
        os.popen(command)


    options = Options()
    options.add_experimental_option(f"debuggerAddress", f"{ip}:{port}")
    driver = webdriver.Chrome(options=options)
    return driver


if __name__  in ['__main__','tools.vpn']:

    session = requests.Session()

    try:
        vpnConfig = getConfig('vpn')
        chromePath = vpnConfig['chromePath']
        ip = vpnConfig['ip']
        port = vpnConfig['port']
        urlList = vpnConfig['urlList']
        retry = vpnConfig['retry']
        mode = getConfig('public')['mode']
        subconverterPath = getConfig('public')['subconverterPath']
        # server_ip = getIp()
    except:
        print('配置获取失败')




    
    
