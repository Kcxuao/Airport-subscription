import logging, os, sys
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

sys.path.append('./tools/')
from tools import vpn,vpn2
from tools.utils import getWords, getConfig, getBalance


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('运行start')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getWords())


async def runV1Bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('运行run')
    
    try:
        arg = (update['message']['text']).split(" ")
        password = arg[1]
        choice = int(arg[2])
        balance = getBalance()
    except:
        os.popen('pkill Google')
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="参数错误"
        )


    if password != botPassword:
        print('运行失败--密码错误')
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="密码错误"
        )

    if balance < 20:
        print('余额不足')
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"余额不足 当前余额为: 「 {balance} 」"
        )

    # 正常运行
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="开始运行"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"当前余额为: 「 {balance} 」"
    )

    url = vpn.run(choice)
    if url:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=url
        )
    else:
         await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"获取失败"
        )


async def runV2Bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('运行v2')

    try:
        arg = (update['message']['text']).split(" ")
        choice = int(arg[1])
    except:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="参数错误"
        )
    
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="开始运行"
    )

    try:
        url = vpn2.run(choice)
        
        print(url)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=url
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='获取失败'
        )
    

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('运行help')
    text = """
它可以做什么？
    获取机场订阅链接并转换为surfboard格式

如何使用？
    /start              问好
    /run[密码][索引]  启动[模式一]
    /run_v2 [索引]   启动[模式二]
    /run_trans      启动订阅转换服务
    /stop_trans     停止订阅转换服务
    /help             显示当前帮助文档
    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=constants.ParseMode.HTML)
    

async def run_trans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('启动订阅转换服务')
    text= ''

    # 启动订阅转换服务
    os.system(f'pkill subconverter')
    flag = os.system(f'nohup {subconverterPath} > ./log/subconverter.log 2>&1 &')
    if flag == 0:
        text = '订阅转换服务启动成功'
    else:
        text = '订阅转换服务启动失败'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def stop_trans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('停止订阅转换服务')
    text= ''

    # 启动订阅转换服务
    flag = os.system(f'pkill subconverter')
    if flag == 0:
        text = '订阅转换服务停止成功'
    else:
        text = '订阅转换服务停止失败'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)



if __name__ == '__main__':
    token = getConfig('telegram')['token']
    botPassword = getConfig('telegram')['botPassword']
    subconverterPath = getConfig('public')['subconverterPath']

    if token == None or botPassword == None:
        print("配置读取错误")
    else:
        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler('start', start)
        run_handler = CommandHandler('run', runV1Bot)
        runv2_handler = CommandHandler('run_v2', runV2Bot)
        help_handler = CommandHandler('help', help)
        run_trans_handler = CommandHandler('run_trans', run_trans)
        stop_trans_handler = CommandHandler('stop_trans', stop_trans)

        application.add_handler(start_handler)
        application.add_handler(run_handler)
        application.add_handler(help_handler)
        application.add_handler(runv2_handler)
        application.add_handler(run_trans_handler)
        application.add_handler(stop_trans_handler)

        application.run_polling()
