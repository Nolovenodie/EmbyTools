from sdk.emby import EmbyService
from sdk.ranks_draw import RanksDraw
from telegram.bot import Bot, Request
from telegram import ParseMode

# 配置项
config = {
    # Emby Url
    "host": "",
    # Emby Apikey
    "api_key": "",
    # Bot setting
    "bot_key": None, # 为 None 无需推送, 否则请设为 Bot 密钥
    "bot_proxy": "",  # "http://127.0.0.1:7890/",
    "send_channel": "@FreeEmbyUpdate",
    "send_group": "@FreeEmbyGroup",
    # 向前获取数据的天数
    "days": 7,
}

# 初始化对象
emby = EmbyService(config["host"], config["api_key"])
draw = RanksDraw(emby)

# 获取数据
success, movies = emby.get_report(types=emby.PLAYBACK_REPORTING_TYPE_MOVIE, days=config["days"], limit=5)
if not success:
    exit(movies)
success, tvshows = emby.get_report(types=emby.PLAYBACK_REPORTING_TYPE_TVSHOWS, days=config["days"], limit=5)
if not success:
    exit(tvshows)

# 绘制海报
draw.draw(movies, tvshows)
path = draw.save()

# 发送海报
if not config["bot_key"]:
    exit("无需推送, 运行结束, 海报: " + path)
proxy = Request(proxy_url=config["bot_proxy"])
bot = Bot(token=config["bot_key"], request=proxy)
text = "🌟*过去7日观影排行*\r\n\r\n"
text += "🏷 \#WeeklyRanks\r\n"
text += "💫 [» 𝙈𝙞𝙨𝙩𝙮 «](t.me/FreeEmby) 丨 [» 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 «](t.me/FreeEmbyChannel)"
msg = bot.send_photo(
    chat_id=config["send_channel"],
    photo=open(path, "rb"),
    caption=text,
    parse_mode=ParseMode.MARKDOWN_V2
)
bot.forward_message(
    chat_id=config["send_group"],
    from_chat_id=config["send_channel"],
    message_id=msg.message_id
)
