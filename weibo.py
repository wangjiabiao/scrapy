# coding=utf-8
'''
看下接口的稳定性和速度，是否容易被ban,目前程序被ban(需要加代理)，但是其他网页手机没啥问题

vps的间隔时间会导致代理失效,增加重试次数和最大时长，也增加请求间隔时间
'''
import requests
import json
import pymongo
import time
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

headers = {"User-Agent": "okhttp/3.8.1", 'Host': 'api.weibo.cn',}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3226.400 QQBrowser/9.6.11681.400",
    'Host': 'api.weibo.cn', 'Connection': 'keep-alive'}
client = pymongo.MongoClient("mongodb://root:testd123xmt@10.19.20.38:27017/")
db = client["testing"]
collection = db.weibo
url = "https://api.weibo.cn/2/statuses/user_timeline?since_id=0&c=weicoandroid&source=211160679&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&count=30&uid=1840551510&feature=0&from=1055095010&feature=1"
url = "https://api.weibo.cn/2/statuses/user_timeline?c=weicoandroid&source=211160679&access_token=2.00WpOZID06XASO004085e4f8de88UE&count=30&uid=1650111241&feature=0&from=1055095010&max_id=4138767792830463 "
# url="https://api.weibo.cn/2/statuses/user_timeline?since_id=0&c=weicoandroid&source=211160679&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&count=30&uid=2054942695&feature=0&from=1055095010"
# url="https://api.weibo.cn/2/statuses/user_timeline?c=weicoandroid&source=211160679&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&count=30&uid=2054942695&feature=0&from=1055095010&max_id=3974744212170684"
url = "http://api.weibo.cn/2/statuses/user_timeline?since_id=0&s=f5eaeaaf&source=211160679&c=weicoandroid&gsid=_2A250jirpDeTxGeRO4lMX9C_NyDuIHXVVGjkhrDV6PUJbjdANLUzbkWqYy6xnARmCgvnQhtWIFvpM5tep0A..&base_app=0&count=20&uid=1840551510&feature=0&from=1055095010&page=1&trim_user=1&max_id=0"
# res = requests.get(url, headers={"User-Agent": "okhttp/3.8.1"}).content
# print(json.loads(res))
# "https://api.weibo.cn/2/cardlist?v_f=2&c=weicoabroad&source=4215535043&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&lang=zh_CN&count=15&containerid=100303type%3D1%26t%3D1%26q%3D%E5%B8%B8%E6%98%8A&extparam=tuid%25253D0&from=1073095010&page=1"

##获取长微博的接口
weibourl = "https://api.weibo.cn/2/statuses/show?c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&id=4112322803526006&isGetLongText=1"

##获取评论的接口
commenturl = "https://api.weibo.cn/2/comments/build_comments?s=bc554dbf&is_reload=1&c=weicoabroad&source=4215535043&gsid=_2A250jq0ADeTxGeRO4lMX9C_NyDuIHXVVHafIrDV6PUJbjdANLXndkWpIaA0YLvPUMKJXgSrTKMHACnYzNA..&id=4112322803526006&count=30" \
             "&is_show_bulletin=2&from=1073095010&v_p=43&flow=0&max_id=0"

job = "http://api.51job.com/api/job/get_job_info.php?jobid=92653733&accountid=60665198&key=8789feb80037a110d1ce5968a6fb816b598ba604&from=searchjoblist&jobtype=0&productname=51job&partner=a534fea33b6f53e802faffc9b7d829c5&uuid=8e3d4accb77354937aa4ec0c2bcb46f6&version=722&guid=d21bee01c500d1e696f1db58ac79124c "

##关注者
friendUrl = "https://api.weibo.cn/2/friendships/friends?cursor=0&count=30&uid=5747171209&c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP"

##被关注着
followerUrl = "https://api.weibo.cn/2/friendships/followers?cursor=0&count=30&uid=5747171209&c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP"
followerUrl = "https://api.weibo.cn/2/friendships/followers?cursor=210&count=30&uid=5747171209&c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP"


# 获取单个用户的所有微博（原创），保存到mongo。如果该用户已经爬取过，则只会更新(需要传入最大微博id)。

def getuserWeibo(uid):
    if collection.find_one({"user.id": uid}) is not None:
        pass
    else:
        isnext = True
        max_id = None
        while isnext is True:
            time.sleep(0.5)
            if max_id is None:
                url = "https://api.weibo.cn/2/statuses/user_timeline?c=weicoandroid&source=211160679&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&uid={}&feature=1&from=1055095010&feature=1&page=1".format(
                        uid)
            else:
                url = "https://api.weibo.cn/2/statuses/user_timeline?max_id={}&c=weicoandroid&source=211160679&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&uid={}&feature=1&from=1055095010&feature=1&page=1".format(
                        max_id, uid)
            print url
            r = requests.get('http://127.0.0.1:8899/api/proxy/get/', timeout=10)
            proxy = r.json()
            print proxy
            try :
               res = s.get(url, headers=headers, verify=False,
                               proxies={"https": "https://" + proxy["proxy"] + ":8889"},timeout=7).content
            except requests.exceptions.ProxyError:
               print 1

               res = s.get(url, headers=headers, verify=False,timeout=7).content
            except:
               break
            print res
            data = json.loads(res)
            max_id = data.get("next_cursor")
            print max_id
            if len(data.get("statuses")) >= 1:
                for d in data.get("statuses"):
                    time.sleep(0.25)
                    # print d.get("isLongText")
                    if d.get("isLongText") == False:
                        collection.insert_one(d)

                    else:
                        # print d.get("id")
                        text = getlongText(d.get("id"))
                        d["text"] = text
                        collection.insert_one(d)


            else:
                pass
            isnext = True if max_id > 0 else False


##获取某个用户的最大页数
def getfollwer(uid, maxpage=1):
    url = "https://api.weibo.cn/2/friendships/followers?cursor=0&count=30&uid={}&c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP".format(
            uid)
    print url
    r = requests.get('http://127.0.0.1:8899/api/proxy/get/', timeout=10)
    proxy = r.json()
    res = s.get(url, headers=headers, verify=False,
                       proxies={"https": "https://" + proxy["proxy"] + ":8889"}).content
    data = json.loads(res)
    next = data.get("next_cursor")
    print next
    for u in data.get("users"):
        yield u.get("id")


###获取长微博的正文
def getlongText(id):
    weibourl = "https://api.weibo.cn/2/statuses/show?c=weicoandroid&source=211160679&from=1055095010&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&id={}&isGetLongText=1".format(
            id)
    print weibourl
    r = requests.get('http://127.0.0.1:8899/api/proxy/get/', timeout=10)
    proxy = r.json()
    print proxy
    try :
      res = s.get(weibourl, headers=headers, verify=False,
                       proxies={"https": "https://" + proxy["proxy"] + ":8889"},timeout=10)
    except requests.exceptions.ProxyError:
        res = s.get(weibourl, headers=headers, verify=False,timeout=7).content
    except:
        pass
    print res.status_code
    data = json.loads(res.content)
    print data
    text = data.get("longText").get("content")
    return text


###根据搜索得到相关的用户信息
def getuid(id):
    url = "https://api.weibo.cn/2/cardlist?v_f=2&c=weicoabroad&source=4215535043&access_token=2.0046_YRC06XASOb4bb6ab9dd0xQ9fP&lang=zh_CN&count=15&containerid=100303type%3D17%26q%3D%E6%95%B0%E6%8D%AE&extparam=tuid%25253D0&from=1073095010&page=1"
    # url="https://api.weibo.cn/2/profile?uid=2636621191&s=bc554dbf&c=weicoabroad&source=211160679&from=1055095010&gsid=_2A250jq0ADeTxGeRO4lMX9C_NyDuIHXVVHafIrDV6PUJbjdANLXndkWpIaA0YLvPUMKJXgSrTKMHACnYzNA"


if __name__ == '__main__':
    # getuserWeibo("1730866981")
    getuserWeibo("3037284894")
    # for u in getfollwer("1642585887"):
    #     getuserWeibo(u)
    # print collection.find_one({"user.id":1720962692})
    # getlongText(4113581631104517)
