import psutil
import requests, socket
import yaml
import os
import random
from threading import Thread
from fake_useragent import UserAgent
from webdav3.client import Client
from webdav3.exceptions import LocalResourceNotFound


def getConfig(filename):
    """获取配置文件参数

    Args:
        filename: 配置项

    Returns:
        配置项
    """
    yamlPath = "config/user/config.yaml"

    with open(yamlPath, 'r', encoding='utf-8') as f:
        config = f.read()

    try:
        res = yaml.load(config, Loader=yaml.FullLoader)  # 用load方法转字典
        return res[filename]
    except:
        return None


def createStr(n):
    """生成n位数字字符串

    Args:
        n: 需要生成的字符串位数

    Returns:
        n位字符串
        example:
            621873667
    """
    strs = ''
    for i in range(n):
        strs += str(random.randrange(0, 10))
    return strs


def createEmail(format='', num=8):
    """生成邮箱

    Args:
        flag: 0 没有域名; 1 生成域名 
        num: 邮箱长度

    Returns:
        邮箱号码
        example:
            621873667@qq.com
    """
    list = ['@qq.com', '@163.com', '@gmail.com']

    if format:
        list = [format]
    
    return createStr(num) + random.choice(list)


def getWords():
    """每日一句

        调用一言API获取美句，API官网：https://hitokoto.cn/

    Returns:
        字符串
        example:
            恰沐春风共同游，终只叹，木已舟。
    """
    res = requests.get('https://v1.hitokoto.cn/').json()
    content = res['hitokoto']
    title = res['from']
    return f"{content}\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t-- {title}"


def getClientKey():
    """获取clientKey

        获取 ./yesCaptcha/config.js 中的clientKey属性

    Returns:
        clientKey字符串
        example:
            cdwf123139bdac5db74qwe2d0a68730d770773sad2312
    """
    with open('yesCaptcha/config.js', 'r', encoding='UTF-8') as f:
        config = f.read()

    return config.split("clientKey: '")[1].split("',")[0]


def getBalance():
    """获取余额

    Returns:
        余额字符串
        example:
            -1: 查询失败
            int: 余额
    """
    data = {
        "clientKey": getClientKey()
    }

    res = requests.post(
        'https://china.yescaptcha.com/getBalance', data=data).json()
    if res['errorId'] == 0:
        return res['balance']
    else:
        return -1


def getHeaders(url):
    headers = {}
    headers['user-agent'] = UserAgent().random
    headers['Referer'] = url
    headers['origin'] = url
    return headers


def save(url, filename):
    try:
        savePath = getConfig('webdav')['savePath']
        mode = getConfig('public')['mode']
        format = getConfig('public')['format']
    except:
        print('配置读取错误')
        return False
    
    if mode not in ['surfboard']:
        print('该模式不支持webdav，将以URL模式返回')
        return False

    try:
        print('开始保存文件...')
        res = requests.get(url, timeout=60).text

        with open(savePath + filename + format, 'w') as f:
            f.writelines(res)

        print('保存成功')
    except:
        print('保存失败')
        return False
    return True


def getIp():
    r"""
    多网卡情况下，根据前缀获取IP
    测试可用：Windows、Linux，Python 3.6.x，psutil 5.4.x
    ipv4/ipv6 地址均适用
    注意如果有多个相同前缀的 ip，只随机返回一个
    """
    localIP = ''
    dic = psutil.net_if_addrs()
    for adapter in dic:
        snicList = dic[adapter]
        for snic in snicList:
            if not snic.family.name.startswith('AF_INET'):
                continue                
            ip = snic.address
            if ip.startswith('192.168'):
                localIP = ip
     
    return localIP    


class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def upload(filename):
    print('正在上传文件到webdav...')

    try:
        config = getConfig('webdav')
        options = config['options']
        uploadPath = config['uploadPath']
        savePath = config['savePath']
        format = getConfig('public')['format']
    except:
        print('配置读取错误')
        return False

    try:
        client = Client(options)
        client.upload(uploadPath + filename + format, savePath + filename + format)
        # 打印结果，之后会重定向到log
        print('文件上传成功: ' + filename + format)
        return True
    except:
        print('文件上传失败: ' + filename + format )
        return False


def isExist(str):

    list = getConfig('openai')['image_str_list']

    for i in list:
        if i in str:
            return True

    return False


def getImage():
    print('获取图片')

    try:
        mode = getConfig('image')['mode']
        resp = requests.get(url=f"https://moe.jitsu.top/img/?sort={mode}&type=json")
        return resp.json()['pics'][0]
    except:
        return "没有找到图片呢 (*>﹏<*)"


def getVideo():
    print('获取视频')

    resp = requests.get(url=f"https://tucdn.wpon.cn/api-girl/index.php?wpon=json")
    return "https:" + resp.json()['mp4']
