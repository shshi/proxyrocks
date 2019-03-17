#-*- coding: utf-8 -*-
import flask
import urllib.request as u
import base64
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddr = db.Column(db.String(100))
    location = db.Column(db.String(100))

    def __init__(self, ipaddr, location):
        self.name = ipaddr
        self.email = location
    def __repr__(self):
        return '<User %r>' %self.location
  
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
	</div>
	<style>	
	table, th, td {
	font-family: arial, sans-serif;
	border: 1px solid #dddddd;
	border-collapse: collapse;
	}

	table tr:nth-child(odd) {
	background-color: #eee;
	height:40px;
	}
	table tr:nth-child(even) {
	background-color: #fff;
	height:40px;
	}
	table th {
	background-color: #4f4f4f;
	color: white;
	height:70px;
	}	
	</style>
	
	<table>
		<tr>
			<th>服务器<br>Server Addr.</th>
			<th>端口<br>Port</th>
			<th>密码<br>Password</th>			
			<th>加密方法<br>Encryption</th>
			<th>协议<br>Protocol</th>			
			<th>备注<br>Remarks</th>
		</tr>		
'''%city
    list_postfix='''
	</table>
</body>
<p style="font-size:14px">------<br>* 使用说明：在
  <a href = "https://github.com/shadowsocks/shadowsocks-windows/releases" style=" color:#4f4f4f">
  https://github.com/shadowsocks/shadowsocks-windows/releases</a>
  (Windows)或
  <a href = "https://github.com/shadowsocks/ShadowsocksX-NG/releases" style=" color:#4f4f4f">
  https://github.com/shadowsocks/ShadowsocksX-NG/releases</a>
  (MacOS)下载Shadowsocks的最新版zip文件，解压后打开Shadowsocks，按照上表提供的信息输入对应的服务器、端口和密码，核对加密方法后确定。
  点击任务栏托盘的小飞机图标，选择“启用系统代理”，“系统代理模式”选择为“全局模式”。打开浏览器验证是否成功，否则重新换一行服务器信息。
  <br>* 建议添加多个服务器信息，方便用网不畅时快捷切换服务器。
</p>
<br>
<br>
<div align="center" >
  <a href = "https://wx2.sinaimg.cn/mw690/4d20f2cfgy1g140et5ke9j20ee0eemyr.jpg" style=" color:#c6a300; font-size:30px;">
  <img src="https://wx4.sinaimg.cn/mw690/4d20f2cfgy1g15sbcj8wtj20a70fa401.jpg" width="15%"></a>
</div>
<br><br><br><br><br>
<html>'''
    for i in lst:
        try:
            base64_encode_str = i[6:]
            decode_str = base64_decode(base64_encode_str)
            parts = decode_str.split(':')
            if len(parts) != 6:
                print('不能解析SSR链接: %s' % base64_encode_str)

            server = parts[0]
            port = parts[1]
            protocol = parts[2]
            method = parts[3]
            obfs = parts[4]
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

            obfsparam = base64_decode(param_dic['obfsparam'])
            protoparam = base64_decode(param_dic['protoparam'])
            remarks = base64_decode(param_dic['remarks'])
            if 'SSRTOOL_' in remarks:
                remarks=remarks.replace('SSRTOOL_','')
            group = base64_decode(param_dic['group'])

            lst_item='''
			<tr>
				<td>%s</td>	<!--服务器地址-->
				<td>%s</td>	<!--端口-->
				<td>%s</td>	<!--密码-->
				<td>%s</td>	<!--加密方法-->
				<td>%s</td>	<!--协议-->
				<td>%s</td>	<!--备注-->
			</tr>
			'''%(server, port, password, method, protocol, remarks)
            #lst_item='<td>服务器地址: %s, 端口: %s, 协议: %s, 加密方法: %s, 密码: %s, 混淆: %s, 混淆参数: %s, 协议参数: %s, 备注: %s, 分组: %s</td>'% (server, port, protocol, method, password, obfs, obfsparam, protoparam, remarks, group)
            list_sum+=lst_item           
        except Exception as e:
            #print (e)
            continue
    list_sum+=list_postfix
    #print (list_sum)
    return list_sum
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
    app.debug = True
    app.run().getList()
    print("finished")    


