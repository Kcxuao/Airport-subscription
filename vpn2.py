import pprint
from utils import getConfig, createEmail, createStr, save, upload
import requests
from urllib import parse
import json, time


def register(url):
    print('开始注册...')

    headers = {}
    headers['content-type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=data).content.decode('utf-8')
        res = json.loads(res)
        print('注册成功')
        print(res)
        return res['data']['auth_data']
    except:
        return False


def login(url):
    print('开始登录')
    for i in range(retry):
        try:
            res = requests.post(url, data=data).content
            res = json.loads(res.decode('utf-8'))

            print('登录成功')
            return res['data']['auth_data']
        except:
            print('token获取失败，正在重试中...')
    return None


def getUrl(url, token):
    print('正在获取订阅...')

    headers = {}
    headers['authorization'] = token

    res = requests.get(url, headers=headers).content.decode('utf-8')
    res = json.loads(res)

    print('订阅获取成功')
    return res['data']['subscribe_url']


def createUrl(subscribe_url):
    print('订阅转换成功')
    url = f"https://sub.xeton.dev/sub?target=surfboard&url={subscribe_url}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini"
    return url


def run(i):

    urls = urlList[i]
    registerUrl = urls['url'] + '/api/v1/passport/auth/register'
    subscribeUrl = urls['url'] + '/api/v1/user/getSubscribe'
    loginUrl = urls['url'] + '/api/v1/passport/auth/login'
  
    token = register(registerUrl)
    if token == False:
        token = login(loginUrl)

    subscribe_url = getUrl(subscribeUrl, token)
    vpnUrl = createUrl(subscribe_url)


    flag = save(vpnUrl, urls['name'])
    if not flag:
        return vpnUrl
    
    flag2 = upload(urls['name'])
    if not flag2:
        return vpnUrl
    
    return '上传成功'


if __name__ in ['__main__', 'vpn2']:

    try:
        vpnConfig = getConfig('vpn2')
        urlList = vpnConfig['urlList']
        retry = vpnConfig['retry']
    except:
        print('配置获取失败')

    data = {
        'email': createEmail(1, 9),
        'password': createStr(10)
    }
