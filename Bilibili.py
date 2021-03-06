# -*- coding: utf-8 -*-
# @Author: Moid
# @Date:   2020-04-19 18:30:33
# @Last Modified by:   Jingyuexing
# @Last Modified time: 2020-05-23 00:14:45

import json,time
import urllib3
from damuku import parserDamuku
http = urllib3.PoolManager()

dataType = {
    "xml": "application/xml",
    "html": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "xhtml": "application/xhtml+xml",
    "json": "application/json, text/plain, */*",
    "text": "text/plain",
    "webp": "image/webp",
    "png": "image/apng"
}
head = {
    "Sec-Fetch-Mode": "no-cors",
    "Cache-Control": "max-age=0",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}
with open("data/API.json", "r", encoding='utf-8') as file:
    api = json.loads(file.read())
    file.close()


def requests(method='', url='', param={}):
    '''
    发起请求
    =======

    [description]

    Keyword Arguments:
        method {str} -- 方式(POST|GET|DELETE) (default: {''})    
        url {str} -- 链接 (default: {''})    
        parma {dict} -- 参数 (default: {{}})    

    Returns:
        {dict} -- 返回数据
    '''
    req = http.request(method=method, url=url, fields=param, headers=head)
    if (req.status == 200):
        return json.loads(req.data.decode("utf-8"), encoding='utf-8')


def getRank(rankID=0, day=3, typer=1, arc_type=0):
    '''
    获取排行榜

    [description]

    Keyword Arguments:
        rankID {number} -- [description] (default: {0})
        day {number} -- [description] (default: {3})
        typer {number} -- [description] (default: {1})
        arc_type {number} -- [description] (default: {0})

    Returns:
        [type] -- [description]
    '''
    config = api[0]
    method = config['method']
    url = config['link']
    parma = {
        "rid": rankID,
        'day': day,
        'type': typer,
        'arc_type': arc_type,
        'jsonp': 'jsonp'
    }
    return requests(method=method, url=url, fields=parma)


def getUserInfor(userid=0):
    '''获取用户信息

    [description]

    Keyword Arguments:
        userid {number} -- [description] (default: {0})

    Returns:
        [type] -- [description]
    '''
    config:dict = api[2]
    method = config["method"]
    url = config["link"]
    parma = {
        "mid":str(userid),
        "jsonp": "jsonp"
    }
    return requests(method=method, url=url, param=parma)


def getFanList(userID=0, pageNumber=1, limit=20):
    '''获取粉丝列表

    [description]

    Keyword Arguments:
      userID {number} -- 用户id (default: {0})
      pageNumber {number} -- 列表页数 (default: {1})
      limit {number} -- 信息条数 (default: {20})

    Returns:
      {dict} -- 返回的数据
    '''
    config:dict = api[3]
    method = config['method']
    url = config['link']
    parma = {
        "vmid": userID,
        "pn": pageNumber,
        "ps": limit,
        "order": "desc",
        "jsonp": "jsonp"
    }
    return requests(method=method, url=url, fields=parma)


def getUserVedioList(userID=0, limit=50, tagID=0, pageNumber=1, order='pubdate'):
    '''获取用户视频列表

    [description]

    Keyword Arguments:
        userID {number} -- 用户ID (default: {0})
        limit {number} -- 限制数,能获取的视频列表条数 (default: {50})
        tagID {number} -- 标签ID (default: {0})
        pageNumber {number} -- 页数 (default: {1})
        order {str} -- 未知 (default: {'pubdate'})

    Returns:
        {json} -- 返回的数据
    '''
    config = api[5]
    method = config['method']
    url = config['link']
    parma = {
        'mid': userID,
        'ps': limit,
        'pn': pageNumber,
        'order': order,
        'jsonp': 'jsonp'
    }
    return requests(method=method, url=url, parma=parma)


def getHistoryMsg(tp=1, oid=0, date=0):
    '''[summary]

    获取历史弹幕

    Keyword Arguments:
        tp {number} -- 类型 (default: {1})
        oid {number} -- 视频oid号 (default: {0})
        date {number} -- 日期 日期格式为 YYYY-MM-dd (default: {0})
    Returns:
        {XML} -- 服务器返回的数据

        例如以下的数据格式

    ```html
        <d p="567.37200,1,25,16777215,1587435278,0,ea1a2aa0,31610950691848199">哈哈哈哈哈哈</d>
    ```

    '''
    config = api[7]
    method = config['method']
    url = config['link']
    parma = {
        'type': tp,
        'oid': oid,
        'date': date
    }
    req = http.request(method=method, url=url, fields=parma)
    if req.status == 200:
        return parserDamuku.Danmaku(req.data)


def getVedioStat(vedioID=0):
    '''获取视频的硬币 分享 喜欢

    [description]

    Keyword Arguments:
        vedioID {number} -- [description] (default: {0})
    '''
    config = api[8]
    url = config['link']
    method = config['method']
    param = {
        'aid': vedioID
    }
    return requests(method=method, url=url, param=param)


def getVedioInfo(bvid=0, avid=0):
    '''[summary]

    获取视频信息

    Keyword Arguments:
        bvid {number} -- BV号 (default: {0})
        avid {number} -- av号 非必须 (default: {0})
        av号和bv号任选一种
    Returns:
        {json} -- 服务器返回的数据
    '''
    config = api[7]
    url = config['link']
    method = config['method']
    if bvid != '':
        parma = {
            'bvid': bvid
        }
    else:
        parma = {
            "avid": avid
        }
    return requests(method=method, url=url, param=parma)


def uploadImage(img: str = '', imgType: str = "daily"):
    '''上传图片

    [description]

    Keyword Arguments:
        img {str} -- 文件名 (default: {''})
        imgType {str} -- 文件类型 (default: {"daily"})

    Returns:
        {dict} -- 返回JSON数据
    '''
    config = api[9]
    method = config['method']
    url = config['link']
    param = {
        'file_up': img,
        'category': imgType
    }
    data = requests(method=method, url=url, param=param)
    if(data != None and data['message'] == 'success'):
        return data['data']


def getRoomInfo(userID=0):
    '''获取用户直播间信息

    [description]

    Keyword Arguments:
        userID {number} -- 用户mid (default: {0})

    Returns:
        {dict} -- 返回信息
    '''
    config = api[10]
    method = config['method']
    url = config['link']
    param = {
        'mid': userID
    }
    return requests(method=method, url=url, param=param)


def getLoginUrl():
    config = api[11]
    method = config['method']
    url = config['link']
    return requests(method=method, url=url)


def checkNickName(nickName: str = ""):
    '''检查昵称是否存在

    [description]

    Keyword Arguments:
        nickName {str} -- 昵称 (default: {""})

    Returns:
        {dict} -- 返回信息
    '''
    config = api[13]
    method = config['method']
    url = config['link']
    param = {
        'nickName': nickName
    }
    return requests(method=method, url=url, param=param)


def getFollowsList(userID=0, limit=50, pageNumber=1):
    '''获取粉丝数

    若登陆则可获取全部粉丝数

    Keyword Arguments:
        mid {number} -- 用户id (default: {0})
        limit {number} -- 每次获取条数 (default: {50})
        pageNumber {number} -- 页码 (default: {1})

    Returns:
        [type] -- [description]
    '''
    config = api[14]
    url = config['link']
    method = config['method']
    param = {
        'vmid': userID,
        'ps': limit,
        'pn': pageNumber
    }
    return requests(method=method, url=url, param=param)


def getBlackList(btype=None, otype=0, pageNumber=1):
    config = api[16]
    method = config['method']
    url = config['link']
    param = {
        'btype': btype,
        'otype': otype,
        'pn': pageNumber
    }
    return requests(method=method, url=url, param=param)


def getBlockedInfo(userID=0):
    '''获取被禁用户的详情

    [description]

    Keyword Arguments:
        mid {number} -- 用户mid (default: {0})

    Returns:
        {dict} -- JSON
    '''
    config = api[17]
    method = config['method']
    url = config['link']
    param = {
        "id": userID
    }
    return requests(method=method, url=url, param=param)


def getArticleInfo(articleID=0):
    '''获取专栏信息

    [description]

    Keyword Arguments:
        articleID {number} -- 专栏id (default: {0})

    Returns:
        {json} -- 返回的数据
    '''
    config = api[15]
    method = config['method']
    url = config['link']
    param = {
        'id': articleID
    }

    return requests(method=method, url=url, param=param)


def getOnlineNumber():
    '''获取在线人数

    '''
    config = api[18]
    method = config['method']
    url = config['link']
    return requests(method=method, url=url)


def getMyselfInfo():
    pass


def getUserInfoCard(userID):
    config = api[28]
    url = config['link']
    method = config['method']
    param = {
        'mid': userID
    }
    return requests(method=method, url=url, param=param)


def getShortInfo():
    pass


def searchUserVedio():
    pass


def sendMsg(yourID, elseID, content=''):
    '''发送消息

    给别人发送消息

    Arguments:
        yourID {int} -- 你的ID
        elseID {int} -- 对方的ID

    Keyword Arguments:
        content {str} -- 发送的消息的内容 (default: {''})

    Returns:
        {json} -- 回应消息
    '''
    config = api[19]
    method = config['method']
    url = config['link']
    param = {
        "msg[sender_uid]": yourID,
        "msg[receiver_id]": elseID,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        "msg[msg_status]": 1,
        "msg[content]": {
            "content": content
        }
    }
    return requests(method=method, url=url, param=param)


def isLike(avID=None, bvID=""):
    config = api[21]
    method = config['method']
    url = api['link']
    if(avID != None):
        param = {
            'aid': avID
        }
    return requests(method=method, url=url, param=param)


def isCoins(avID=None, bvID=""):
    '''是否投币

    [description]

    Keyword Arguments:
        avID {int} -- AV号 (default: {None})
        bvID {str} -- BV号 (default: {""})

    Returns:
        [type] -- [description]
    '''
    config = api[22]
    method = config['method']
    url = api['link']
    if(bvID != None):
        param = {
            'aid': avID
        }
    return requests(method=method, url=url, param=param)


def isFavorite(avID=None, bvID=""):
    """视频是否收藏

    [description]

    Keyword Arguments:
        avID {int} -- 视频AV号 (default: {None})
        bvID {str} -- 视频BV号 (default: {""})

    Returns:
        {json} -- 返回的JSON数据
    """
    config = api[23]
    method = config['method']
    url = api['link']
    param = {
        'aid': avID
    }
    return requests(method=method, url=url, param=param)


def getRelations(userID=0):
    config = api[29]
    url = config['link']
    method = config['method']
    param = {
        "fids": userID,
        "jsonp": "jsonp"
    }
    return requests(method=method, url=url, param=param)


def vedioTagDelete(AID=0, tagID=0):
    '''需要在登陆情况下操作

    删除标签

    Keyword Arguments:
        AID {number} -- 视频的aid号 (default: {0})
        tagID {number} -- 标签的ID (default: {0})

    Returns:
        [type] -- [description]
    '''
    config = api[30]
    url = config['link']
    method = config['method']
    param = {
        "aid": AID,
        "tag_id": tagID,
        "jsonp": "jsonp"
    }
    return requests(method=method, url=url, param=param)


def getDanmuku(cid: int=None):
    config = api[31]
    url = config['link'].format(cid=cid)
    method = config['method']
    data = parserDamuku.Danmaku(requests(method=method, url=url))
    return data


class Vedio(object):
    """docstring for Vedio"""
    avid = 0
    bvid = ''
    cover = ''
    tagID = 0
    title = ''
    oid = 0
    tag = ''
    owner = 0
    createTime = 0
    coin = 0
    like = 0
    favorite = 0
    share = 0
    view = 0
    reply = 0

    def __init__(self, vedioID=''):
        if(vedioID != ''):
            data = getVedioInfo(bvid=vedioID)
            if(data != None):
                data = data['data']
                self.avid = data['aid']
                self.bvid = data['bvid']
                self.tag = data['tname']
                self.tagID = data['tid']
                self.title = data['title']
                self.cover = data['pic']
                self.oid = data['cid']
                self.owner = data['owner']['mid']
                self.createTime = data['ctime']
                self.view = data['stat']['view']
                self.favorite = data['stat']['favorite']
                self.coin = data['stat']['coin']
                self.share = data['stat']['share']
                self.like = data['stat']['like']
                self.reply = data['stat']['reply']

    def getVedio(self):
        return self

    def getUser(self):
        return User(self.owner)

    def getDamku(self):
        return getDanmuku(self.cid)

    def sendDamku(self,color:str = '#ffffff',fontsize:int = 25,mode:int = 1,pool:int = 1,content:str = ''):
        '''发送弹幕
        [description]
        Keyword Arguments:
            color {str} -- 弹幕颜色 (default: {''})
            fontsize {int} -- 字体大小 (default: {25})
            mode {int} -- 1 滚动 |5 顶部 |4 底部 (default: {1})
            pool {int} -- 字幕弹幕 1 是 0否 (default: {1})
            content {str} -- 弹幕内容 (default: {''})
        Returns:
            [type] -- [description]
        '''
        config = api[24]
        method = config['method']
        url    = config['link']
        param = {
            'type':1,
            'oid':self.oid,
            'bvid':self.bvid,
            'msg':content,
            'progress':int(time.time()),
            'color':color,
            'fontsize':fontsize,
            'pool':pool,
            'mode':mode,
            'plat':'1'
        }
        return requests(method,url,param)

    def isCoins(self):
        return isCoins(avID=self.avid)

    def isFavorite(self):
        return isFavorite(avID=self.avid)

    def isLike(self):
        return isLike(avID=self.avid)


class Article:

    def __init__(self,):
        pass


class User(object):
    """docstring for User"""
    mid:int = 0
    name:str = ''
    sex:str = ''
    face:str = ''
    birthday:str = ''
    rank:int = 0
    level:int = 0
    vip:bool = False

    def __init__(self, userid=0):
        if(userid != 0):
            data = getUserInfor(userid=userid)
            if(data != None):
                data = data['data']
                self.mid = data['mid']
                self.name = data['name']
                self.sex = data['sex']
                self.birthday = data['birthday']
                self.level = data['level']
                self.rank = data['rank']
                self.face = data['face']
                self.vip = bool(data['vip']['type'])