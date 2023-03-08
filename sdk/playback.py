import pytz
import sqlite3
from datetime import datetime, timedelta

PLAYBACK_REPORTING_TYPE_MOVIE = "ItemName"
PLAYBACK_REPORTING_TYPE_TVSHOWS = "substr(ItemName,0, instr(ItemName, ' - '))"


class PlaybackReporting:
    def __init__(self, db_file):
        self.db_file = db_file

    def _open_db_(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def _close_db_(self):
        self.cursor.close()
        self.conn.close()

    def get_report(self, types=PLAYBACK_REPORTING_TYPE_MOVIE, user_id=None, days=7, end_date=datetime.now(pytz.timezone("Asia/Shanghai")), limit=10):
        sub_date = end_date - timedelta(days=days)
        start_time = sub_date.strftime("%Y-%m-%d 00:00:00")
        end_time = end_date.strftime("%Y-%m-%d 23:59:59")
        sql = "SELECT UserId, ItemId, ItemType, "
        sql += types + " AS name, "
        sql += "COUNT(1) AS play_count, "
        sql += "SUM(PlayDuration - PauseDuration) AS total_duarion "
        sql += "FROM PlaybackActivity "
        sql += f"WHERE ItemType = '{'Movie' if types==PLAYBACK_REPORTING_TYPE_MOVIE else 'Episode'}' "
        sql += "AND DateCreated >= ? AND DateCreated <= ? "
        sql += "AND UserId not IN (select UserId from UserList) "
        if user_id:
            sql += "AND UserId = ? "
        sql += "GROUP BY name "
        sql += "ORDER BY play_count DESC "
        sql += "LIMIT ?"
        try:
            self._open_db_()

            param = (start_time, end_time, )
            if user_id:
                param += (user_id, )
            param += (limit, )

            self.cursor.execute(sql, param)
            rows = self.cursor.fetchall()
            self._close_db_()
            return True, rows
        except Exception as e:
            return False, "🤕执行时出现错误 >> " + str(e)
