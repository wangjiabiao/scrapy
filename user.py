#coding=utf-8
###需要用户的id和登陆后分配的token即可，哈哈，未知的是tocken的失效时间
###需要深度爬取全站的用户关系，需要考虑下
import requests,json
headers = {'content-type': 'application/json',
           "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER",
         'Host':'www.timeface.cn',
'Origin':'http://www.timeface.cn',
'Referer':'http://www.timeface.cn/login'
  }
headers1={'content-type': 'application/json',
           "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER",
         'Host':'www.timeface.cn',
'Origin':'http://www.timeface.cn',
'Referer':'http://www.timeface.cn/user/591407277240/fans',
'tf-token':'eef9212b7de60431ba5115cb226c7910',
'tf-uid':'591407277240'
  }
logininfo = {"account":'505279206@qq.com',"password":'NTJscDEzMTQ=','type': 0,'f': ""
              }
# r = requests.post("http://www.timeface.cn/tf/auth/login",
#                            data=json.dumps(logininfo),
#                            headers=headers,
#                            )
# print r.content
#
# data=r.content.get('data')
# r=requests.post("http://www.timeface.cn/tf/member/followlist",data=json.dumps({"uid":"578095887307","pageSize":10,"pageNumber":1}),
#
#                 headers=headers1)
# print r.content
# for d in json.loads(r.content).get('data').get('datas'):
#     print d

r=requests.post("http://www.timeface.cn/tf/member/fanslist",data=json.dumps({"uid":"591407277240","pageSize":10,"pageNumber":1}),

                 headers=headers1)
print r.content
# for d in json.loads(r.content).get('data').get('datas'):
#     print d
##获取某个user的follows或者fans，返回详情
def get_follow(userid,type="follow"):
    headers={'content-type': 'application/json',
           "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER",
         'Host':'www.timeface.cn',
'Origin':'http://www.timeface.cn',
'Referer':'http://www.timeface.cn/user/591407277240/fans',
'tf-token':'eef9212b7de60431ba5115cb226c7910',
'tf-uid':'591407277240'
  }
    try:
     #print "http://www.timeface.cn/tf/member/%slist"%(type)
     r=requests.post("http://www.timeface.cn/tf/member/%slist"%(type),data=json.dumps({"uid":userid,"pageSize":10,"pageNumber":1}),headers=headers)
     #print r
     content=json.loads(r.content)

     totalRecord=content.get('data').get('totalRecord')
     r=requests.post("http://www.timeface.cn/tf/member/%slist"%(type),data=json.dumps({"uid":userid,"pageSize":totalRecord,"pageNumber":1}),headers=headers)
     content=json.loads(r.content)
    except Exception ,e:
     print e
     content=None
    if content:
     if content.get('code')==u'000':
       return content.get('data').get('datas')

    else:
       return  []



import pymongo,time
con = pymongo.Connection('139.196.51.73',27017)

db = con.spiderdb
##广度遍历,简单的for会死循环下去
def get_followall(startid,type="follow"):
    #users=get_follow(startid)
    queue = []
    all=set()
    queue.append(startid)
    #all.add(startid)
    while len(queue)>0:
        u=queue.pop()
        if u not in all  :
          all.add(u)
          d=get_follow(u,type=type)
          print d
          if d:
           db.tfuser1.insert({"user":u,"fans":d})
           #time.sleep(0.5)
           for dd in d:
              #all.add(startid)
              if  dd.get('fans')>0 and dd.get('uid')!=startid :
                #print 1
                queue.append(dd.get('uid'))
                #all.add(dd.get('uid'))
              else:
                pass
        #print u.get('uid'),u.get('followers')

        # if u.get('uid') not in all and u.get('followers')>0:
        #     print  get_follow(u.get('uid'))
        #     db.tfuser.insert({"user":u.get('uid'),"follow":get_follow(u.get('uid'))})
        #     all.append(u.get('uid'))
        #     get_followall(u.get('uid'))
        # else:
        #     pass
#get_followall("591407277240",type='fans')
#print get_follow("342495873258",type='follow')


####
def get_usrall(startid):
    #users=get_follow(startid)
    queue = []
    all=set()
    queue.append(startid)
    #all.add(startid)
    while len(queue)>0:
        u=queue.pop()
        fans_id=[]
        follow_id=[]

        if u not in all  :
          all.add(u)
          follow=get_follow(u,type="follow")
          fans=get_follow(u,type="fans")
          if not isinstance(follow,list) :
             follow=[]
          if not isinstance(fans,list) :
             fans=[]

          follow_id=[e.get('uid') for e in follow] if len(follow)>0 else []
          fans_id=[e.get('uid') for e in fans] if len(fans)>0 else []
          ids=follow_id+fans_id
          users=follow+fans
          #print d

          db.tfuser_relation.insert({"user":u,"f`ans":fans_id,"follows":follow_id})

          #time.sleep(0.5)
          for id in ids:
              #all.add(startid)
              print id
              #print db.tfuser.find({'user_id':id}).count()
              if  db.tfuser.find({'uid':id}).count() >0 :
                print 1
                pass
              else:
                #print users[ids.index(id)]
                db.tfuser.insert(users[ids.index(id)])
                queue.append(id)
                #all.add(dd.get('uid'))

get_usrall("591407277240")
con.close()
