import os
from sdk.ranks_draw import RanksDraw
from sdk.emby import EmbyService
from sdk.playback import *

# 配置项
config = {
    # Emby Url
    "host": "",
    # Emby Apikey
    "api_key": "",
    # 改为你的 playback_reporting 数据库文件位置, 默认不用更改， 一般为 /var/lib/emby/data/playback_reporting.db
    "db_file": os.path.join("var", "lib", "emby", "data", "playback_reporting.db"),
    # 向前获取数据的天数
    "days": 7,
}

# 初始化对象
emby = EmbyService(config["host"], config["api_key"])
report = PlaybackReporting(config["db_file"])
draw = RanksDraw(emby)

# 获取数据
success, movies = report.get_report(types=PLAYBACK_REPORTING_TYPE_MOVIE, days=config["days"], limit=5)
if not success:
    exit(movies)
success, tvshows = report.get_report(types=PLAYBACK_REPORTING_TYPE_TVSHOWS, days=config["days"], limit=5)
if not success:
    exit(tvshows)

# 绘制海报
draw.draw(movies, tvshows)
draw.save()
