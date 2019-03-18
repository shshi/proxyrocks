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
    #list_sum=''
    lst_SSR=[]
    lst_qrcode=[]
    for i in lst:
        try:
            qrcode_i='https://api.qrserver.com/v1/create-qr-code/?size=100x100&data='+i
            #qrcode_i='<a href=%s><img src=%s></a>&nbsp;'%(qrcode,qrcode)
            lst_qrcode.append(qrcode_i)
            #lst_SSR+='<a style="font-size:10px;">%s</a><br>'%i
            lst_SSR.append(i)
        except Exception as e:
            print (e)
            
    #list_sum+=lst_SSR
    #list_postfix=''
    #list_sum+=list_postfix

    return render_template('index.html', **locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True).getList()
    print("finished")    

