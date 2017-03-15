import requests
import json
import time
import random
from common import *

def loginYima():
	url='http://api.51ym.me/UserInterface.aspx'
	body={
		'action':'login',
		'username':'gc12306',
		'password':'gaochong1513'
	}
	r=requests.get(url,params=body)
	result=r.text.split('|')
	token=result[1]
	return token


def getMobile(token):
	url='http://api.51ym.me/UserInterface.aspx'
	body={
		'action':'getmobile',
		'token':token,
		'itemid':'2730'
	}
	r = requests.get(url, params=body)
	result=r.text.split('|')
	if result[0]=='success':
		mobile=result[1]
		return mobile
	else:
		return ""
def releaseAll(token):
	url='http://api.51ym.me/UserInterface.aspx'
	body={
		'action':'releaseall',
		'token':token
	}
	r = requests.get(url, params=body)
	return r.text
def getMessage(token, mobile, itemid):
	print ("get message.")
	url='http://api.51ym.me/UserInterface.aspx'
	body={
		'action':'getsms',
		'mobile':mobile,
		'itemid':itemid,
		'token':token
	}
	sms="3001"
	while sms=='3001':
		r=requests.get(url,params=body)
		sms=r.text
		print ("message:%s"%sms)
		time.sleep(5)
	sms=sms.split('|')[1]
	print (sms)
	begin = sms.find(':')+1
	end = sms.find(',')
	code=sms[begin:end]
	return code
		
	

def getCode(mobile, only):
	#print (only)
	url1='http://api.gb6m.com/index/index.php?c=index&m=user&a=do_app'
	mdata={
		'only':only
	}
	r=requests.post(url1, data=mdata)
	#print (r.headers['Set-Cookie'])
	cookie=r.headers['Set-Cookie']
	result = json.loads(r.text)
	url='http://api.gb6m.com/index/index.php'
	body={
		'c':'index',
		'm':'user',
		'a':'send_mobile_code'
	}
	proxies = {
		'http' : '222.134.134.250:8118'
	}   
	mdata={
		'mobile':mobile
	}
	headers={
		'User-Agent':'ZHIXIAO_A',
		'Host':'api.gb6m.com',
		'Cookie':cookie
	}
	time.sleep(5)
	#response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(mdata)) 
	r = requests.post(url,headers=headers,params=body, data=mdata)
	
	#print(response)
	result = json.loads(r.text)
	status = result['status']
	return cookie, status