import time
from requests_html import HTMLSession
import json

def get_contests():
    session = HTMLSession()
    d = {"operationName":None,"variables":{},"query":"{\n  allContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    duration\n    originStartTime\n  }\n}\n"}
    r = session.post("https://leetcode-cn.com/graphql/", json=d)
    val = json.loads(r.text)
    data = val["data"]
    contests = data["allContests"]
    v = 0
    ret = {}
    for c in contests[::-1]:
        ret[v] = c["title"]
        v += 1
    return ret

from .structs.user import User
def get_user_info(user_name):
    session = HTMLSession()
    d = {"operationName":"userPublicProfile","variables":{"userSlug":""},"query":"query userPublicProfile($userSlug: String!) {\n  userProfilePublicProfile(userSlug: $userSlug) {\n    username\n    profile {\n      realName\n      ranking {\n        ranking\n        currentLocalRanking\n        ratingProgress\n      }\n    }\n  }\n}\n"}
    d["variables"]["userSlug"] = user_name
    r = session.post("https://leetcode-cn.com/graphql/", json=d)
    val = json.loads(r.text)
    data = val["data"]["userProfilePublicProfile"]
    if data == None:
        # No such user
        return None
    profile = data["profile"]
    if profile["ranking"] == None:
        # Never participate in contest
        return None
    user = User()
    user.user_name = user_name
    user.real_name = profile["realName"]
    user.local_ranking = int(profile["ranking"]["currentLocalRanking"])
    rating = profile["ranking"]["ratingProgress"]
    ranking = json.loads(profile["ranking"]["ranking"])
    REMOVE_CONTEST = 86
    rating = rating[REMOVE_CONTEST:]
    ranking = ranking[REMOVE_CONTEST:]

    user.rating = []
    user.ranking = []
    user.contest_idx = []
    for i in range(len(ranking)):
        if ranking[i] == 0:
            continue
        user.rating.append(rating[i])
        user.ranking.append(ranking[i])
        user.contest_idx.append(i)

    return user

from .structs.ranklist_page import RanklistPage, RanklistUser
def get_ranklist_page(page):
    session = HTMLSession()
    d = {"operationName": None,"variables":{},"query":"{\n  localRanking(page: " + str(page) + ") {\n    totalUsers\n    userPerPage\n    rankingNodes {\n      currentRating\n      user {\n        username\n        profile {\n          realName\n        }\n      }\n    }\n  }\n}\n"}
    r = session.post("https://leetcode-cn.com/graphql/", json=d)
    val = json.loads(r.text)
    data = val["data"]["localRanking"]
    r = RanklistPage()
    r.total_users = int(data["totalUsers"])
    r.user_per_page = int(data["userPerPage"])
    r.users = []
    users = data["rankingNodes"]
    start_ranking = (page - 1) * r.user_per_page + 1
    for i in range(len(users)):
        user = users[i]
        u = RanklistUser()
        u.ranking = start_ranking + i
        u.rating = int(user["currentRating"])
        u.user_name = user["user"]["username"]
        u.real_name = user["user"]["profile"]["realName"]
        r.users.append(u)
    return r

def test_get_ranklist_page(page):
    r = get_ranklist_page(page)
    print("total: ", r.total_users)
    print("user per page: ", r.user_per_page)
    for u in r.users:
        print(u.user_name, u.real_name, u.rating)

def test_get_user_info(user_name):
    cont = get_contests()
    u = get_user_info(user_name)
    print(u.user_name)
    print(u.real_name)
    print(u.local_ranking)
    print(len(u.ranking))
    assert(len(u.ranking) == len(u.rating))
    for i in range(len(u.ranking)):
        if u.ranking[i] == 0:
            continue
        if i in cont:
            print(i, u.ranking[i], u.rating[i], cont[i])
        else:
            print(i, u.ranking[i], u.rating[i])

def test_contest():
    get_contests()

import sys
if __name__ == "__main__":
    #test_get_ranklist_page(int(sys.argv[1]))
    test_get_user_info(sys.argv[1])
    #test_contest()
