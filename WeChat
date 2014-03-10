# coding=utf-8
from bottle import *
import hashlib
import xml.etree.ElementTree as ET
import urllib2
# import requests
import json
import sae.const
import MySQLdb

MYSQL_DB = sae.const.MYSQL_DB 
MYSQL_USER = sae.const.MYSQL_USER 
MYSQL_PASS = sae.const.MYSQL_PASS 
MYSQL_HOST = sae.const.MYSQL_HOST 
MYSQL_PORT = sae.const.MYSQL_PORT




txt = open('raw-data.txt','rb').readlines()
title = open('title_1.txt','rb').read()
title2 = title.split('\n')
rec = open('rec_num.dat','rb').readlines()
rate_txt = open('rate.txt','rb').read()
title_list = []
for i in title2:
	title_list.append(i.split(':')[0])
#bucket.put_object('3.txt', open(__file__, 'rb'))
#txt = bucket.get_object_contents('1.txt')
#bucket.put()
#chunks = bucket.get_object_contents('2.txt', chunk_size=10)
#stor = sae.storage.Client('rec2txt-rec-text.dat')
#stor.list('rec2txt-rec_text.dat') 


@get("/")
def checkSignature():
    """
    这里是用来做接口验证
    
    """
    token = "happyfeng"  # 你在微信公众平台上设置的TOKEN
    signature = request.GET.get('signature', None)  
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        
        return echostr
    
    else:
        return None
 
 
def parse_msg():
    """
    这里是用来解析微信Server Post过来的XML数据的，取出各字段对应的值，以备后面的代码调用，也可用lxml等模块。
    """
    recvmsg = request.body.read()  # 严重卡壳的地方，最后还是在Stack OverFlow上找到了答案
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

@post("/")
def response_msg():
    """
    这里是响应微信Server的请求，并返回数据的主函数，判断Content内容，如果是一条“subscribe”的事件，就
    表明是一个新注册用户，调用纯文本格式返回，如果是其他的内容就组织数据以图文格式返回。
 
    基本思路：
    # 拿到Post过来的数据
    # 分析数据（拿到FromUserName、ToUserName、CreateTime、MsgType和content）
    # 构造回复信息（将你组织好的content返回给用户）
    """
    # 拿到并解析数据
    msg = parse_msg()
    # 设置返回数据模板
    # 纯文本格式
    #ToUserName开发者微信号
    #FromUserName发送方帐号
    textTpl = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""


    pictextTpl = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%s]]></Url>
                </item>
                </Articles>
                <FuncFlag>1</FuncFlag>
                </xml> """
    # 判断Content内容，如果等于"Hello2BizUser"，表明是一个新关注用户
    if msg["MsgType"] == "event":
        echostr = textTpl % (
            msg['FromUserName'], msg['ToUserName'], str(int(time.time())),
            u"欢迎关注iPaperRec，他将为您推荐您感兴趣的论文，回复‘测试’进行测试，回复任意字符将提示帮助，按要求回复相应的数字编号，并按要求对结果作出评价，累计一定的评价次数，有奖励哦！亲！")
        return echostr
    #连接数据库
    conn=MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASS,db=MYSQL_DB,port=int(MYSQL_PORT))
    cur=conn.cursor()
    

    #用户评价结果，输入评分
    if msg['Content'] in ['a','b','c','d','e']:
        cur.execute('update '+msg['FromUserName']+' set score ="%s" where score is NULL'%msg['Content'])
        conn.commit()
        echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),'谢谢您的评价！回复“测试”可继续使用。')
        return echostr

    #判断若有未评分的用户，要求输入评分，否则不执行后面部分
    cur.execute('create table if not exists  ' + msg['FromUserName'] + '(user_id varchar(20),paper_in int,paper_out int,score varchar(20))')
    Null_number = cur.execute('select paper_out from '+msg['FromUserName']+' where score is NULL and paper_in is not NULL')
    if Null_number > 0:
        cur.execute('select paper_in from '+msg['FromUserName']+' where score is NULL')
        paper_in = cur.fetchone()[0]
        echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),'请输入您对文章 %s 推荐结果的评分，请参照推荐界面图示，回复字母a-e, 分别对应“非常满意、满意、一般、不满意、不确定”。'%paper_in)
        return echostr
    
    if msg['Content'] in title_list:
        content_num = msg['Content']  #标记文章号
    	for y in rec:
            if y.split(':')[0] == msg['Content']:
                num = y.split(':')[1]
        num_list = num[1:-2].split(',')
        titles = txt[int(num_list[3])].split(',')
        
        #判断是否已经评价过
        try:
            paper_in_list = []
            m = cur.execute('select paper_in from '+msg['FromUserName']+' where score is not NULL')
            for i in range(m):
                paper_in_list.append(cur.fetchone()[0])
        except:
            paper_in_list = [0]
        if int(msg['Content']) in paper_in_list:
            echostr = pictextTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),titles[3][1:-1],','.join(titles[4:]),'http://b399.photo.store.qq.com/psb?/531166946/8j0pMRtH5KjQ3Xw7L5U9F9ZS8VfgoG4rJ8O9r4TvE2E!/b/dGPR2.1mDAAA&bo=0AKQAQAAAAABAGQ!&rf=photoDetail','http://scholar.google.com.hk/scholar?q='+'%20'.join(titles[1][1:-1].split(' ')))
            return echostr    
        else:
            #向表插入数据
            cur.execute('insert into '+msg['FromUserName']+' values(%s,%s,%s,%s)',[msg['FromUserName'],int(msg['Content']),int(num_list[3]),None])
            conn.commit()
            echostr = pictextTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),titles[3][1:-1],','.join(titles[4:]),'http://b399.photo.store.qq.com/psb?/531166946/8j0pMRtH5KjQ3Xw7L5U9F9ZS8VfgoG4rJ8O9r4TvE2E!/b/dGPR2.1mDAAA&bo=0AKQAQAAAAABAGQ!&rf=photoDetail','http://scholar.google.com.hk/scholar?q='+'%20'.join(titles[1][1:-1].split(' ')))
            return echostr
    	#echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), rate_txt)
        #return echostr
        
    #输入编号，查看文章
    for paper_n in title_list:
    	if msg['Content'] == u"查看"+paper_n :
            echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),txt[int(paper_n)])
            return echostr
    '''
    #用户评价结果，输入评分
    for rate_n in [1,2,3,4,5]:
        if msg['Content'] ==u'评分'+str(rate_n):
            bucket.put_object(msg['FromUserName']+'.txt',bucket.get_object_contents(msg['FromUserName']+'.txt')+':评分'+str(rate_n)+'\n')
            echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())),'谢谢您的评价！回复“测试”可继续使用。')
            return echostr
    '''
    #输入评分次数，可查看用户已评论过的有效次数    
    if msg['Content'] == u'评价次数':
        n = cur.execute('select * from '+msg['FromUserName']+' where score is not NULL')
        echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), '您有效的评价次数为%s次'%n)
        return echostr
    #开始测试文章
    if msg['Content'] == u'测试':
        echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), '请输入您看过的论文编号,如“2”，为您推荐感兴趣的论文，并按要求对之后的推荐结果做出评价（若忘记了该论文，可输入“查看+编号”，如“查看2”，查看编号为2的文章）：\n'+title)
        return echostr
    else:   
        
        #msg['MsgType'] = 'text'
    	echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), '输入“测试”即可体验该系统，每次需要对推荐结果进行评价，分a-e五个等级，按推荐页面图片提示的要求做。输入“评价次数”可以查看您已经评价过的次数，累计20次有奖励哦！\n')
        #echostr = textTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), rate_txt)
        return echostr

            
if __name__ == "__main__":
    # Interactive mode
    debug(True)
    run(host='127.0.0.1', port=80, reloader=True)

else:
    # Mod WSGI launch
    import sae
    debug(True)
    os.chdir(os.path.dirname(__file__))
    app = default_app()
    application = sae.create_wsgi_app(app)


