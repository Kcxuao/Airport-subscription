import pprint
from utils import getConfig, createEmail, createStr, getHeaders
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

# '06227601@163.com', '4957969861'

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
    headers = getHeaders(urlList[0])

    registerUrl = urlList[i] + '/api/v1/passport/auth/register'
    subscribeUrl = urlList[i] + '/api/v1/user/getSubscribe'
    loginUrl = urlList[i] + '/api/v1/passport/auth/login'
  
    token = register(registerUrl)
    if token == False:
        token = login(loginUrl)

    subscribe_url = getUrl(subscribeUrl, token)
    return createUrl(subscribe_url)


if __name__ in ['__main__', 'vpn2']:

    try:
        vpnConfig = getConfig('vpn2')
        urlList = vpnConfig['url_list']
        retry = vpnConfig['retry']
    except:
        print('配置获取失败')

    data = {
        'email': createEmail(1, 9),
        'password': createStr(10)
    }
