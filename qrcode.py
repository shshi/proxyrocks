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
	少华的贩枪乐园
</title>
</head>
<body>
	<h4>嗨，来自%s的朋友，我是少华，以下代理服务器信息每三天自动更新一次，欢迎体验如丝般顺滑的外网感受。</h4>
	<div>
	<p>使用方法见表尾，如果有问题请联系：shi.sh@foxmail.com&nbsp;&nbsp;
	<img src="https://wx4.sinaimg.cn/mw690/4d20f2cfgy1g15lhprtqkj205l04jaa1.jpg" width="25" alt="" style="vertical-align:bottom">
	<a href = "https://www.weibo.com/omega7" style="color:#4f4f4f;">漂泊的韦恩</a>
	</p>		
'''%city
    for i in lst:
        try:
            qrcode='https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='+i
            lst_item='<img src=%s width="15%">'%qrcode	
            list_sum+=lst_item           
        except Exception as e:
            print (e)
            #continue
    list_postfix='''
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

