import logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import vpn
from utils import getWords, getConfig, getBalance

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getWords())


async def runBot(update: Update, context: ContextTypes.DEFAULT_TYPE):


    try:
        arg = (update['message']['text']).split(" ")
        password = arg[1]
        choice = int(arg[2])
        balance = getBalance()
    except:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="参数错误"
        )


    print(choice)
    if password != 'kcxuao':
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


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
它可以做什么？
    获取机场订阅链接并转换为surfboard格式

如何使用？
    /start         问好
    /run [密码]   启动程序
    /help         显示当前帮助文档
    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=constants.ParseMode.HTML)


if __name__ == '__main__':
    token = getConfig('telegram')['token']
    if token == None:
        print("token错误")
    else:
        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler('start', start)
        run_handler = CommandHandler('run', runBot)
        help_handler = CommandHandler('help', help)

        application.add_handler(start_handler)
        application.add_handler(run_handler)
        application.add_handler(help_handler)

        application.run_polling()
