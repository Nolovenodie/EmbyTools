import requests
from cacheout import Cache

cache = Cache()


class EmbyService():
    def __init__(self, host, api_key):
        self.host = host
        self.base_url = host + "/emby/{0}?api_key=" + api_key
        self.api_key = api_key

    @cache.memoize(ttl=600)
    def primary(self, item_id, width=200, height=300, quality=90, ret_url=False):
        url = self.host + f"/emby/Items/{item_id}/Images/Primary?maxHeight={height}&maxWidth={width}&quality={quality}"
        if ret_url:
            return url
        resp = requests.get(url)

        if resp.status_code != 204 and resp.status_code != 200:
            return False, "🤕Emby 服务器连接失败!"
        return True, resp.content

    @cache.memoize(ttl=600)
    def backdrop(self, item_id, width=1920, quality=70, ret_url=False):
        url = self.host + f"/emby/Items/{item_id}/Images/Backdrop/0?&maxWidth={width}&quality={quality}"
        if ret_url:
            return url
        resp = requests.get(url)

        if resp.status_code != 204 and resp.status_code != 200:
            return False, "🤕Emby 服务器连接失败!"
        return True, resp.content

    @cache.memoize(ttl=600)
    def logo(self, item_id, quality=70, ret_url=False):
        url = self.host + f"/emby/Items/{item_id}/Images/Logo?quality={quality}"
        if ret_url:
            return url
        resp = requests.get(url)

        if resp.status_code != 204 and resp.status_code != 200:
            return False, "🤕Emby 服务器连接失败!"
        return True, resp.content

    @cache.memoize(ttl=300)
    def items(self, user_id, item_id):
        url = self.base_url.format(f"Users/{user_id}/Items/{item_id}")
        resp = requests.get(url)

        if resp.status_code != 204 and resp.status_code != 200:
            return False, "🤕Emby 服务器连接失败!"
        return True, resp.json()


class LibraryService:
    def __init__(self, host, api_key):
        self.base_url = host + "/Library/{0}?api_key=" + api_key

    """
    Gets all user media folders
    """

    @cache.memoize(ttl=600)
    def folders(self):
        url = self.base_url.format("SelectableMediaFolders")
        resp = requests.get(url)

        if resp.status_code != 204 and resp.status_code != 200:
            return False, "🤕Emby 服务器连接失败!"
        return True, resp.json()
