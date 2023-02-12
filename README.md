# Airport-subscription

Airport-subscription是一款自动注册并获取机场订阅、转换订阅链接并推送至Telegram机器人的工具。支持同步至webdav。



# 免责声明

Airport-subscription为python学习交流的开源非营利项目，仅作为程序员之间相互学习交流之用，使用需严格遵守开源许可协议。严禁用于商业用途，禁止使用Airport-subscription进行任何盈利活动。对一切非法使用所产生的后果，我们概不负责。



# 使用方法

## 1、安装python环境

请自行百度



## 2、安装所需依赖

```python
pip install -r requirements.txt

⚠️注意：selenium请选择与自身浏览器相匹配的版本
```



## 3、创建Tg机器人

## 在 Telegram 中创建聊天机器人

1. 登录 Telegram 并转到 https://telegram.me/botfather

2. 点击网页界面中的 **Start** 按钮或输入 /start

3. 点击或输入 **/newbot** 并输入名称

4. 为聊天机器人输入一个用户名，该名称应以“bot”结尾（例如 garthsweatherbot）

5. 复制生成的访问令牌

   

## 4、配置文件参数

路径： config/user/config.yaml

如无需同步至webdav，将会推送订阅链接至Tg机器人中

- 配置Tg机器人参数

  ```yaml
  telegram:
    token: ""  # 将第三步的访问令牌粘贴到此处
  ```



- 配置webdav（可选）

  ```yaml
  webdav:
    uploadPath: /Surfboard/profiles/  # surfboard的webdav备份目录
    savePath: ./urls/  # 下载的订阅保存路径
    options:
      webdav_hostname: ""  # webdav地址
      webdav_login: ""  # 账号
      webdav_password: ""  # 密码
      disable_check: True
  ```

  

- 配置你的订阅网站

  ```yaml
  vpn:
     urlList:    
        [
            {
                name: 'xxx',  # 名字 决定下载的文件名称
                url: 'http://example.com',  # 官网地址，地址后不要带/
            }
            ...
        ]
  ```

  请按照如上格式进行配置



## 5、运行

1. 打开你的机器人，输入/help查看命令列表
2. 执行/run 或 /run_v2



# 运行模式

## /run【索引】

该模式适用与注册时需要谷歌验证的网站

- 参数说明：

  - 密钥：在配置文件中设置的botPassword

    ```yaml
    telegram:
      token: ""  # 机器人TOKEN
      whiteList: [''] # 白名单，添加tg账号
    ```

  - 索引：设置的网站列表索引，从0开始计数

    ```yaml
    urlList: [{...},{...}]  # 索引0则是取出列表第一位
    ```

  

- 配置文件

  1. config/user/config.yaml

     ```yaml
     vpn:
        chromePath: ./Chrome  # 修改为你的谷歌浏览器可执行文件路径
     ```

  2. yesCaptcha/config.js

     官网注册：https://yescaptcha.com/i/TAY9VX

     登录成功后找到 【帐户密钥 ClientKey】复制输入框中的 ClientKey

     ```js
     const config = {
         clientKey: '', // 输入你授权的clientKey
         host: 'https://api.yescaptcha.com', // 服务器地址，默认官网服务器	
     }
     ```



## /run_v2 【索引】

该模式适用于注册时无需谷歌验证的网站

无需额外配置
