#-*- coding: utf-8 -*-
#import os
import flask
import psycopg2
import urllib.request as u
import base64
import json
from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)      
  
@app.route("/")

def getList():
    #f = open("proxyList.log",'w',encoding='utf-8')
    url="https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com"
    page = u.urlopen(url)
    html = page.read().decode('UTF-8')

    SSR_list=base64.b64decode(html).decode('utf-8')
    SSR_list=SSR_list.strip()   
    lst=SSR_list.splitlines()
    try:
        #ip_visitor = request.remote_addr
        if request.headers.getlist("X-Forwarded-For"):
            ip_visitor = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_visitor = request.remote_addr
        print (ip_visitor)
        #response = u.urlopen("http://ip-api.com/json/%s"%ip_visitor).read()
        #raw_geo=response.decode("ascii").replace("\"","").replace("{","").replace("}","")
        #geo = dict(toks.split(":") for toks in raw_geo.split(",") if toks)
        
        response = u.urlopen("http://ip.360.cn/IPQuery/ipquery?ip=%s"%ip_visitor).read()
        geo = json.loads(response)
        print (geo)
        city = geo['data']
        index=city.find('\t')
        if index>0:
            city = city.replace(city[index:],'')
    except Exception as e:
        print (e)
        city="围城里"            
    list_sum='''
<!DOCTYPE html>
<html>
<head>
<title>
	少华的二维码贩枪乐园
</title>
</head>
<body>
	<h4>嗨，来自%s的朋友，我是少华，以下代理服务器信息每三天自动更新一次，欢迎体验如丝般顺滑的外网感受。</h4>
	<div>
	<p>使用方法见页尾，如果有问题请联系：shi.sh@foxmail.com&nbsp;&nbsp;
	<img src="https://wx4.sinaimg.cn/mw690/4d20f2cfgy1g15lhprtqkj205l04jaa1.jpg" width="25" alt="" style="vertical-align:bottom">
	<a href = "https://www.weibo.com/omega7" style="color:#4f4f4f;">漂泊的韦恩</a>
	</p>		
'''%city
    SSR_list='<br><br><a>SSR 列表：</a><br>'
    for i in lst:
        try:
            qrcode='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data='+i
            #lst_item='<img src=%s>&nbsp;'%qrcode
            lst_item='<a href=%s><img src=%s></a>&nbsp;'%(qrcode,qrcode)
            list_sum+=lst_item
            SSR_list+='<a style="font-size:10px;">%s</a><br>'%i
        except Exception as e:
            print (e)
            #continue
    list_sum+=SSR_list
    list_postfix='''

<p style="font-size:14px">------<br>* 使用说明：在
  <a href = "https://github.com/shadowsocksrr/shadowsocksr-csharp/releases" style=" color:#4f4f4f">
  https://github.com/shadowsocksrr/shadowsocksr-csharp/releases</a>
  (Windows)或
  <a href = "https://github.com/shadowsocks/ShadowsocksX-NG/releases" style=" color:#4f4f4f">
  https://github.com/shadowsocks/ShadowsocksX-NG/releases</a>
  (MacOS)
  下载ShadowsocksR的最新版zip文件，解压后打开ShadowsocksR，任务栏托盘里将会有个小飞机，点击上面任意一个二维码后右击小飞机扫描。建议多扫描几个二维码信息备用，方便用网不畅时快捷切换。
  另外一种方法（推荐）：批量复制上面的SSR数据，然后在小飞机上右击选择“从剪切板导入SSR”。<br>
  * 手机端：安卓用户使用<a href = "https://github.com/shadowsocksrr/shadowsocksr-android/releases" style=" color:#4f4f4f">
  ShadowsocksR</a>扫描，苹果用户请使用Potatso Lite(仅见国外账号app store)。
</p>
</body>
<br>
<br>
<div align="center" width="15%">
  <a href = "https://wx2.sinaimg.cn/mw690/4d20f2cfgy1g140et5ke9j20ee0eemyr.jpg" style=" color:#c6a300; font-size:30px;">
  <img src="https://wx4.sinaimg.cn/mw690/4d20f2cfgy1g15sbcj8wtj20a70fa401.jpg" width="15%"></a>
</div>
<br><br><br><br><br>
<html>'''
    list_sum+=list_postfix
    #print (list_sum)
    return list_sum

if __name__ == '__main__':
    app.run(debug=True).getList()
    print("finished")    

