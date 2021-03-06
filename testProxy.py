#-*- coding: utf-8 -*-
import os
import flask
import urllib.request as u
import base64
import json
from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2

app = flask.Flask(__name__)
#DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:2643383@localhost/proxyget')

#app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
#db = SQLAlchemy(app)

class User():
    def __init__(self):
        self.conn = psycopg2.connect(user="postgres", password="2643383", host="127.0.0.1", port="5432", database="proxyget")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_command = "CREATE TABLE test(id serial PRIMARY KEY, server varchar(100), port varchar(100), password varchar(100), method varchar(100), protocol varchar(100), remarks varchar(100))"
        self.cursor.execute(create_table_command)
        
    def insert_new_record(self):
        #new_record=["","","","","","",""]
        #insert_command="INSERT INTO proxy(server, port, password, method, protocol, remarks) VALUES(%s,%s,%s,%s,%s,%s)"
        #print(insert_command)
        #self. cursor.execute(insert_command)
        print ("insert now")
        for record in lst_data:
            try:
                print (record)
                insert_command = """ INSERT INTO test(server, port, password, method, protocol, remarks) VALUES (%s,%s,%s,%s,%s,%s)"""
                self.cursor.execute(insert_command, record)
                count = self.cursor.rowcount
                print (count, "Record inserted successfully into mobile table")
            except (Exception, psycopg2.Error) as error :
                if(self.conn):
                    print("Failed to insert record into mobile table: ", error)
            finally:
                #closing database connection.
                if(self.conn):
                    self.cursor.close()
                    self.conn.close()
                    print("PostgreSQL connection is closed")


@app.route("/")

def getList():
    #f = open("proxyList.log",'w',encoding='utf-8')
    url="https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com"
    page = u.urlopen(url)
    html = page.read().decode('UTF-8')

    lst_SSR=base64.b64decode(html).decode('utf-8')
    lst_SSR=lst_SSR.strip()   
    lst_SSR=lst_SSR.splitlines()
    city=getCity()
    lst_table=parseSSR(lst_SSR)
    global lst_data
    lst_data=lst_table
    return render_template('get.html', **locals())

def getCity():
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
    return city

def parseSSR(lst_SSR):
    lst_table=[]
    for ssr in lst_SSR:
        try:
            base64_encode_str = ssr[6:]
            decode_str = base64_decode(base64_encode_str)
            parts = decode_str.split(':')
            if len(parts) != 6:
                    print('不能解析SSR链接: %s' % base64_encode_str)

            server = parts[0]
            port = parts[1]
            protocol = parts[2]
            method = parts[3]
            #obfs = parts[4]
            password_and_params = parts[5]

            password_and_params = password_and_params.split("/?")

            password_encode_str = password_and_params[0]
            password = base64_decode(password_encode_str)
            params = password_and_params[1]

            param_parts = params.split('&')

            param_dic = {}
            for part in param_parts:
               key_and_value = part.split('=')
               param_dic[key_and_value[0]] = key_and_value[1]

            #obfsparam = base64_decode(param_dic['obfsparam'])
            #protoparam = base64_decode(param_dic['protoparam'])
            remarks = base64_decode(param_dic['remarks'])
            if 'SSRTOOL_' in remarks:
                    remarks=remarks.replace('SSRTOOL_','')
            group = base64_decode(param_dic['group'])

            dic_item=[server, port, password, method, protocol, remarks]
            #print (dic_item)
            #dic_item={server:%s, port:%s, password:%s, method:%s, protocol:%s, remarks:%s}%(server, port, password, method, protocol, remarks)
            #lst_item='服务器地址: %s, 端口: %s, 协议: %s, 加密方法: %s, 密码: %s, 混淆: %s, 混淆参数: %s, 协议参数: %s, 备注: %s, 分组: %s'% (server, port, protocol, method, password, obfs, obfsparam, protoparam, remarks, group)
            lst_table.append(dic_item)
        except Exception as e:
            print (e)
    return lst_table

def fill_padding(base64_encode_str):

   need_padding = len(base64_encode_str) % 4 != 0

   if need_padding:
       missing_padding = 4 - need_padding
       base64_encode_str += '=' * missing_padding
   return base64_encode_str


def base64_decode(base64_encode_str):
   base64_encode_str = fill_padding(base64_encode_str)
   return base64.urlsafe_b64decode(base64_encode_str).decode('utf-8')


if __name__ == '__main__':
    #db_conn=User()
    app.run(debug=True).getList()
    #User().create_table()
    #User().insert_new_record()
    print("finished")    


