const config = {
    clientKey: '', // 你购买授权的clientKey
    host: 'https://api.yescaptcha.com', // 服务器地址，默认官网服务器https://api.yescaptcha.com

    autorun: true, // 自动运行 true or false
    imageclassification: true, // reCaptcha谷歌人机自动识别
    hcaptcha: true, // hCaptchaHC人机自动识别
    imagetotext: true, // Coinlist英文数字人机自动识别
    rainbow: true, // Coinlist排队时粉色按钮自动点击
    times: 100, // 延迟时间，单位毫秒
    isTextCaptcha: true
}

// 以下代码请勿修改
chrome.storage.local.get(['config'], function (result) {
    if (!result.config) {
        chrome.storage.local.set({ config }, () => { })// 存储配置
    }
})