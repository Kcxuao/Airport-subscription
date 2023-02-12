from tools import vpn, vpn2
from tools.utils import getWords, getConfig, getBalance, isExist, getImage, getVideo
import os, sys, logging
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from tools.gptAi import createImageResp, createOpenaiResp

sys.path.append('./tools/')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("运行start")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=getWords())


async def runV1Bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('运行run')

    chat_id = str(update.effective_chat.id)

    try:
        arg = (update['message']['text']).split(" ")
        balance = getBalance()
        choice = int(arg[1])
    except:
        os.popen('pkill Google')
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="参数错误"
        )

    if chat_id not in whiteList:
        logging.info('运行失败--无权访问: ' + chat_id)
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="您没有权限访问"
        )

    if balance < 20:
        logging.info('余额不足')
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
    logging.info('运行v2')

    chat_id = str(update.effective_chat.id)

    try:
        arg = (update['message']['text']).split(" ")
        choice = int(arg[1])
    except:
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="参数错误"
        )

    if chat_id not in whiteList:
        logging.info('运行失败--无权访问: ' + chat_id)
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="您没有权限访问"
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="开始运行"
    )

    try:
        url = vpn2.run(choice)

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
    logging.info('运行help')
    text = """
它可以做什么？
    获取机场订阅链接并转换为surfboard格式

如何使用？
    /start            \t\t问好
    /run i           \t\t启动[模式一]
    /run_v2 i       \t\t启动[模式二]
    /image          \t\t返回一张图片
    /video           \t\t返回一个视频
    /help            \t\t显示当前帮助文档
    """

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=constants.ParseMode.HTML)


async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    prompt = update.message.text

    try:
        if isExist(prompt):
            imageUrl = createImageResp(prompt)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=imageUrl)

        else:
            text = createOpenaiResp(prompt)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="没有找到这个 (*>﹏<*)")


async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        url = getImage()
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="没有找到图片呢 (*>﹏<*)")


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        url = getVideo()
        await context.bot.send_video(
            chat_id=update.effective_chat.id, 
            video=url, read_timeout=60, 
            connect_timeout=60, 
            write_timeout=60, 
            pool_timeout=60
        )
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="没有找到视频呢 (*>﹏<*)")



if __name__ == '__main__':
    token = getConfig('telegram')['token']
    whiteList = getConfig('telegram')['whiteList']
    subconverterPath = getConfig('public')['subconverterPath']

    if token == None:
        logging.info("配置读取错误")
    else:
        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler('start', start)
        run_handler = CommandHandler('run', runV1Bot)
        runv2_handler = CommandHandler('run_v2', runV2Bot)
        help_handler = CommandHandler('help', help)
        video_handler = CommandHandler('video', video)
        image_handler = CommandHandler('image', image)
        chatgpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chatgpt)
        
        application.add_handlers([start_handler, run_handler, help_handler, runv2_handler, chatgpt_handler, image_handler, video_handler])
        application.run_polling()
