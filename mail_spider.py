# * coding=utf-8 *
#https://www.ds54.xyz/torrent/ce2551480accf08f3937865dd00ec965ad1fcb83.torrent
import urllib
#import urllib2
#import urllib.request
from urllib import request, parse
import re
import os
import io
import sys
import imp
import time
from urllib.parse import urlparse
import base64
#import http.cookiejar
import http.cookiejar
import socket
import ssl
import random
import json
import requests


#import socket 
#socket.setdefaulttimeout(5.0)
total_item=0
cur_item_no=0
allpic_x = 0
opener = 0


class Spider:
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬取开关，如果为True继续爬取
        self.switch = True
        #通过CookieJar()类构建一个cookieJar对象，用来保存cookie的值
        cookie = http.cookiejar.CookieJar()
        cookie.clear()
        #通过HTTPCookieProcessor()处理器类构建一个处理器对象，用来处理cookie
        #参数就是构建的CookieJar()对象
        cookie_handler = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(cookie_handler, request.HTTPHandler)
        #opener = request.build_opener(cookie_handler) 
        request.install_opener(opener) 
        self.opener = opener
        #self.db = DbHelp()
        
    def mymkdirs(self, spath):
        if(not os.path.exists(spath)):
            os.makedirs(spath)    

    def printDelimiter(self):
        print ('-'*80);
        
    #打开一个网页
    def getHtml(self, url):
        global cur_item_no
        #try:
        time.sleep(1)
        page = urllib.urlopen(url)
        html = page.read()
        #except IOError:
        #    print 'frequency too high ,please try again late'
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url', url)
        print ('http status:',page.getcode())
        return html
    
    def post(self, url, data):
        global cur_item_no
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
        #'accept-encoding': 'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9', 
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cache-Control':'max-age=0', 
       #'referer': 'https://cn.torrentkitty.app/search/',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'none',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = headers.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = headers)
                req = request.Request(url= url, data= deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=2)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s', url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('post url: ', url)
        print ('http status:',page.getcode())
        return html
    
    def spr_post(self, url, data, timeout = 2):
        global cur_item_no
        headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url, data=deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html
    
    def spr_get(self, url, timeout = 2):
        global cur_item_no
        headers = {
       #'referer': 'https://cn.torrentkitty.app/search/',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        print ('='*80)
        print ('get url: ', url)
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url,  headers = headers, method='GET')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        #print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html
        
    def getHtml3(self, url):
        global cur_item_no
        heads = {
       #'referer': 'https://cn.torrentkitty.app/search/',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
       'sec-ch-ua-mobile': '?0',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'none',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url )               
                req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=2)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s', url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('=================================')
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        return html
    
    def callbackDownload(self, blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        sys.stdout.write('#####'+ '->' + '\b\b\b\b\b')
        sys.stdout.write("%.2f%%"% percent)
        #print "%.2f%%"% percent
    
    def autoDown(self, url, filename, dcallback):
        # try:
            # urllib.urlretrieve(url, filename, dcallback)
        # except urllib.ContentTooShortError,IOError:
            # print 'Network is not good reloading.'
            # time.sleep(1)
            # autoDown(url, filename, dcallback)
        # finally:
            # urllib.urlcleanup()
        #url='http://www.facebook.com/'
        heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
    'Accept-Language':'zh-cn,zh;q=0.5', 
    'Cache-Control':'max-age=0', 
    'Connection':'keep-alive', 
    'Keep-Alive':'115', 
    'Referer':url, 
    'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
        fails = 0
        while True:
            try:
                if fails >= 20:
                    break
                print ("get url:" + url)
                req = urllib2.Request(url, headers = heads)
                print (u'开始发起 %d 次请求: ' % fails)
                response = urllib2.urlopen(req,data=None, timeout=3)
                page = response.read()
            except:
                fails += 1
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            else:
                break
        #response=urllib2.Request(url)
        #rs=urllib2.urlopen(response)
        f=open(filename,'wb')#以二进制写模式打开,rb+:以二进制读写模式打开 
        f.write(page)
        f.close()
    
    #获取网页里的图片
    def getImg2_(self, html):
        global allpic_x
        reg = r'<dd>(.+?\.jpg)<dd>'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        s = set(imglist) #用一个集合去除重复
        pic_savepath = r'E:\myzhpic\x2'
        #os.path.join(pic_savepath, )
        #x = 0
        mymkdirs(pic_savepath)
        for imgurl in s:
            print (u"%s --> %s.jpg" % (imgurl, allpic_x))
            autoDown(imgurl, '%s\\%s.jpg' % (pic_savepath, allpic_x), self.callbackDownload)
            print 
            allpic_x+=1
            time.sleep(1)
        

    
    #获取图片
    def getImg(self, imgurl):
        global allpic_x
        print ("get "+ imgurl)
        #/picture/5ee8f061d4bc13bdf0e9fc6f846982a863486af9/01914.jpg
        reg = r'/picture/(\w+?)/(\d+?).jpg'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, imgurl)
        print ("============ getImg ==============")
        print (imglist)
        s = set(imglist) #用一个集合去除重复
        pic_savepath = os.getcwd()
        #os.path.join(pic_savepath, )
        #x = 0
        #mymkdirs(pic_savepath)
        for img in imglist:
            filename = img[0]+"_"+img[1]+'.jpg'
            print (u"%s --> %s" % (imgurl, filename))
            self.autoDown(imgurl, '%s\%s' % (pic_savepath, filename), self.callbackDownload)
            print ()
            allpic_x+=1
            time.sleep(1)
            
    def get_plain_text(self, jsStr):
        #jsStr='6aKc5YC85LiN6ZSZ5b6h5aeQ55u05pKtIOa/gOaDheiHquaFsOWkp+engA=='
        a = base64.b64decode(jsStr)
        re.escape(a)
        s = unquote(a)
        #print(s.decode("utf8"))
        return s.decode("utf8")

       

    

        
    def decode_x_content(self, str):
        text = str.replace(',oc','\\u') 
        text = text.replace(u'\\u00a0', u' ')
        text = text.replace(u'\\u2200', u' ')
        text = text.replace(u'\\u260e', u' ')
        text = text.replace(u'\\ufe0f', u' ')
        text = text.replace(u'\\u2006', u' ')
        text = text.replace(u'\\u2795', u' ')
        #print(text.encode('utf-8').decode('unicode_escape'))
        #return text.encode('utf-8').decode('unicode_escape')
        return text.encode("utf-8").decode('unicode_escape', 'ignore').encode('gbk', 'ignore').decode('gbk')
           


    def ungzip(self, data):
        try:
            data = gzip.decompress(data)
        except Exception as e:
            print('未经压缩, 无需解压')
            pass  # print('未经压缩, 无需解压')
        return data
        
    def spr_post_file(self, url, data, timeout = 2):
        global cur_item_no
        headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
       'Accept-Language': 'zh-CN,zh;q=0.9',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       #'Host': 'certsign.realtek.com',
       #'Origin': 'https://certsign.realtek.com',
       #'Content-Type': 'application/x-www-form-urlencoded',
       #'Referer': 'https://certsign.realtek.com/SMSOTP.jsp',
       'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
       'sec-ch-ua-mobile': '?1',
       'sec-fetch-dest':'document',
       'sec-fetch-mode':'navigate',
       'sec-fetch-site': 'same-origin',
       'sec-fetch-user':'?1',
       'upgrade-insecure-requests':'1',
       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    #'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        #'Cookie': '_pk_ses.2.a6f7=1; JSESSIONID=50CB9A0B10EAC7F72F84B66923CC2E21; _pk_id.2.a6f7=a596b944cc4c029a.1620272182.15.1623237968.1623236515.'
        }
        # 用于模拟http头的User-agent
        ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        ]
        #user_agent = random.choice(ua_list)
        
        #opener.addheaders = heads.items() 
        #url = "https://cn.torrentkitty.app/search/"
        opener = self.opener
        #print ("get url:" + url )
        #page = opener.open(url)
        #ssl._create_default_https_context = ssl._create_unverified_context
        deal_data = bytes(parse.urlencode(data), encoding='utf8')
        fails = 0
        while True:
            try:
                if fails >=100 : 
                    break
                #req = request.Request(url, headers = heads)
                req = request.Request(url, data=deal_data, headers = headers, method='POST')               
                #req.add_header('User-Agent', user_agent)
                page = request.urlopen(req, timeout=timeout)
                html = page.read()
            except urllib.error.HTTPError as error:
                print('Data not retrieved because %s\nURL: %s'%( error, url))
            except request.URLError as e:
                if isinstance(e.reason, socket.timeout):
                    print ('Time out')
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u'网络连接出现问题, 正在尝试再次请求: ', fails)
                time.sleep(1)
            except socket.timeout as error: 
                print('socket timed out - URL %s'% url)
                fails += 1
                if fails >= 20:
                    time.sleep(2+fails-20)
                print (u' 正在尝试再次请求: ', fails)
                time.sleep(1)                
            except ssl.SSLError as e:
                fails += 1
                print ('The read operation timed out, retry ', fails)
            else:
                break
        
        print ('='*80)
        print (u'正在获取第 %d 项数据' % cur_item_no)
        cur_item_no+=1
        print ('get url: ', url)
        print ('http status:',page.getcode())
        print ('='*80)
        return html
        
    def dl_mail(self, username, password):
        '''
        print("Uploading file Win720210604.zip")
        html = self.putFileToCertSign(url="https://certsign.realtek.com/advanceConvert", path="D:\\test", file_name="Win720210604.zip", timeout=60)
        data ={
        'login_username': 'jingdong_qiu',
        'login_password': 'Qq369369'
        }
        html = self.post(url="https://certsign.realtek.com/Login", data=data)
        print(html.decode("utf-8"))
        self.printDelimiter()
        data =[
           ("flag", "otp_c"),
           ("flag", "null")
        ]
        #https://certsign.realtek.com/ADVerify?flag=otp_c&flag=null
        html = self.spr_post("https://certsign.realtek.com/ADVerify",data, 6)#测过浏览器完成这个request大概要5.16s
        print(html.decode("utf-8"))
        '''
        self.printDelimiter()
        
        data1 = {
        'destination': 'https://mail.realtek.com/owa',
        'flags': 4,
        'forcedownlevel': 0,
        'username': username,
        'password': password,
        'isUtf8': 1
        }
        html = self.spr_post(url="https://mail.realtek.com/owa/auth.owa", data=data1);
        html = self.ungzip(html)
        #print(html.decode("utf-8"))
        self.printDelimiter()
        #html = self.getHtml3("https://mail.realtek.com/owa/?ae=Folder&t=IPF.Note&id=LgAAAACZpfPyFZDkTIBBuJbamineAQB3JuyQcogkSZTumckl5UoQAAAApGXlAAAB&slUsng=0")
        #print(html.decode("utf-8"))
       
        respHtml = html.decode("utf-8");
        #<input type="checkbox" name="chkmsg" value="RgAAAACZpfPyFZDkTIBBuJbamineBwB3JuyQcogkSZTumckl5UoQAAAApGXlAABmstg4X0+IQL1SPLvPP4CPAAFbGrirAAAJ" title="&#36873;&#25321;&#39033;&#30446;" onclick="onClkChkBx(this);">&nbsp;</td><td nowrap class="frst">motp@realtek.com&nbsp;</td>
        foundTokenVal = re.search("<input type=\"checkbox\" name=\"chkmsg\" value=\"(?P<id>[^>]+)\" title=\"[^>]+\" onclick=\"[^>]+\">&nbsp;</td><td nowrap( class=\"frst\")?>motp@realtek.com&nbsp;<[^>]+>", respHtml) #(.*)motp@realtek.com
        bFindMOTP = False
        tokenVal=""
        if(foundTokenVal):
            tokenVal = foundTokenVal.group("id")
            print ("=> ",tokenVal)
            bFindMOTP = True
        else:
            print("not found")
        
        if(bFindMOTP):
            url_id = parse.quote(tokenVal)
            url = "https://mail.realtek.com/owa/?ae=Item&t=IPM.Note&id=%s"% url_id
            #rspHtml = self.getHtml3(url)
            html = self.spr_get(url)
            #rspHtml = self.getHtml3("https://mail.realtek.com/owa/?ae=Item&t=IPM.Note&id=RgAAAACZpfPyFZDkTIBBuJbamineBwB3JuyQcogkSZTumckl5UoQAAAApGXlAABmstg4X0%2bIQL1SPLvPP4CPAAFbGrjJAAAJ") 
            print(html.decode("utf-8"))
            rspHtml = html.decode("utf-8")
            #<font color="#0000FF">995253</font>
            foundOtpVal = re.search("<font color=\"#0000FF\">(?P<otp>\d{6})</font>",rspHtml)
            if(foundOtpVal):
                otpcode = foundOtpVal.group("otp")
                print("otp 码：", otpcode)
                self.printDelimiter()
                return otpcode

        

        self.printDelimiter()
        return None
        
'''
if __name__ == "__main__":
    imp.reload(sys)
    #sys.setdefaultencoding('utf8')
    iSpider = Spider()
    #s = duanziSpider.get_urlcode_text()
    #duanziSpider.getcityList()
    iSpider.dl_mail()
'''
