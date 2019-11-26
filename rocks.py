#-*- coding: utf-8 -*-
import os
import flask
#import psycopg2
import urllib.request as u
import base64
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)      
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://eoykghvzwktdrs:b05e54b628df4e1af727bee934b776e2070aaf5577d1197621657f8f80e14bb3@ec2-50-19-109-120.compute-1.amazonaws.com:5432/dd4h8eue8st3b1')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(100))

  def __init__(self, name, email):
    self.name = name
    self.email = email
    
@app.route("/")
def getList():
    #f = open("proxyList.log",'w',encoding='utf-8')
    url="https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com"
    url="https://raw.githubusercontent.com/ssrsub/ssr/master/ssrsub"
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

    return render_template('rocks.html', **locals(), users=User.query.all())

@app.route('/user', methods=['POST'])
def user():
  u = User(request.form['name'], request.form['email'])
  db.session.add(u)
  db.session.commit()
  return redirect(url_for('getList'))

if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True).getList()
    print("finished")    

