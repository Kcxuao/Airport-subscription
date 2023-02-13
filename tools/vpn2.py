import pprint
from .utils import getConfig, createEmail, createStr, save, upload, getIp
import requests
from urllib import parse
import json, time, os


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

    url = f'https://sub.id9.cc/sub?target={mode}&new_name=true&url={subscribe_url}&insert=false&config=https%3A%2F%2Fraw.githubusercontent.com%2FACL4SSR%2FACL4SSR%2Fmaster%2FClash%2Fconfig%2FACL4SSR_Online.ini'
    return url


def run(i):

    # 获取URL并生成相应的URL链接
    urls = urlList[i]
    registerUrl = urls['url'] + '/api/v1/passport/auth/register'
    subscribeUrl = urls['url'] + '/api/v1/user/getSubscribe'
    loginUrl = urls['url'] + '/api/v1/passport/auth/login'

    # 注册成功后获取用户TOKEN
    token = register(registerUrl)
    if token == False:
        # 注册失败（莫名情况）尝试登录
        token = login(loginUrl)

    # 获取转换后的链接
    subscribe_url = getUrl(subscribeUrl, token)
    vpnUrl = createUrl(subscribe_url)

    # 启动订阅转换服务
    # os.popen('pkill subconver')
    # os.popen(f'nohup {subconverterPath} > ./log/subconverter.log 2>&1 &')
    
    # 保存订阅文件到本地
    flag = save(vpnUrl, urls['name'])
    if not flag:
        # 保存失败返回订阅链接，用户手动输入
        return vpnUrl

    
    # 上传订阅文件到webdav，便于用户同步
    flag2 = upload(urls['name'])
    if not flag2:
        # 上传失败返回订阅链接，用户手动输入
        return vpnUrl

    # 关闭订阅转换服务
    # os.popen('pkill subconver')
    
    return '上传成功'


if __name__ in ['__main__', 'tools.vpn2']:

    try:
        vpnConfig = getConfig('vpn2')
        urlList = vpnConfig['urlList']
        retry = vpnConfig['retry']
        mode = getConfig('public')['mode']
        subconverterPath = getConfig('public')['subconverterPath']
        ip = getIp()
    except:
        print('配置获取失败')


    data = {
        'email': createEmail(),
        'password': createStr(10)
    }

