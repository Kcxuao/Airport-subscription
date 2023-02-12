import os
import requests
from .utils import getConfig, isExist


def createOpenaiResp(prompt: str):

    print('开始检索：' + prompt)

    data = {
        "prompt": prompt,
        **completion_params
    }

    try:
        with requests.post(url="https://api.openai.com/v1/completions", json=data, headers=headers, timeout=30) as resp:
            return resp.json()['choices'][0]['text']
    except:
        return "这个我不知道呢～～"


def createImageResp(prompt: str):

    print('开始查找图片：' + prompt)

    data = {
        "prompt": prompt,
        **image_params
    }

    try:
        with requests.post(url="https://api.openai.com/v1/images/generations", json=data, headers=headers, timeout=30) as resp:
            return resp.json()['data'][0]['url']
    except:
        if "safety system" in resp.json()['error']['message']:
            return "这个可不能告诉你哦～～"



if __name__ in ['__main__', 'tools.gptAi']:

    info = getConfig('openai')
    api_key = info['api_key']
    completion_params = info['completion_params']
    image_params = info['image_params']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {api_key}'
    }
