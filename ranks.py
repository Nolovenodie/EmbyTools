import os
from sdk.emby import EmbyService
from sdk.ranks_draw import RanksDraw

# 配置项
config = {
    # Emby Url
    "host": "",
    # Emby Apikey
    "api_key": "",
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
draw.save()
