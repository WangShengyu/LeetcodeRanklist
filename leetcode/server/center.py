from . import robot
import time
class Center():
    def __init__(self):
        self._rank_pages = {}
        self._users = {}
        self._contests = {}

        self._rank_pages_last_sec = {}
        self._rank_page_expire_sec = 60 * 60
        self._users_last_sec = {}
        self._user_expire_sec = 60 * 60
        self._contests_last_sec = -1
        self._contests_expire_sec = 60 * 60

    @staticmethod
    def cur():
        return time.time()

    def _rank_page_expire(self, page):
        if page not in self._rank_pages_last_sec:
            return True
        if Center.cur() - self._rank_pages_last_sec[page] > self._rank_page_expire_sec:
            return True
        return False

    def _user_expire(self, user_name):
        if user_name not in self._users_last_sec:
            return True
        if Center.cur() - self._users_last_sec[user_name] > self._user_expire_sec:
            return True
        return False

    def _contests_expire(self):
        if Center.cur() - self._contests_last_sec > self._contests_expire_sec:
            return True
        return False

    def _get_rank_page_cache(self, page):
        if self._rank_page_expire(page):
            self._rank_pages[page] = robot.get_ranklist_page(page)
            self._rank_pages_last_sec[page] = Center.cur()
        return self._rank_pages[page]

    def _get_contests_cache(self):
        if self._contests_expire():
            self._contests = robot.get_contests()
            self._contests_last_sec = Center.cur()
        return self._contests

    def _get_user_info_cache(self, user_name):
        if self._user_expire(user_name):
            self._users[user_name] = robot.get_user_info(user_name)
            self._users_last_sec[user_name] = Center.cur()
        return self._users[user_name]

    def get_rank_page(self, page):
        rank_page = self._get_rank_page_cache(page)
        return rank_page

    def get_user(self, user_name):
        cont = self._get_contests_cache()
        user = self._get_user_info_cache(user_name)
        if user == None:
            return None
        user.contest_name = [""] * len(user.contest_idx)
        for i in range(len(user.contest_idx)):
            idx = user.contest_idx[i]
            if idx in cont:
                user.contest_name[i] = cont[idx]

        return user
