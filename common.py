import random
import requests
import json
import time
import math
import requests

class Util(object):
	def luhn_check(self, num):
		digits = [int(x) for x in reversed(str(num))]
		check_sum = sum(digits[1::2]) + sum((dig//10 + dig%10) for dig in [2*el for el in digits[::2]])
		return (10-check_sum%10)%10
	def gen_imme(self):
		TAC='867922'
		FAC='02'
		SNR=565583
		imme=TAC+FAC+str(SNR+random.randint(1,1000))
		return (imme+str(self.luhn_check(imme)))

	def visit(self, url, body, cookie): 
		headers = { 'User-Agent' : 'ZHIXIAO_A',
					'Content-type': 'application/x-www-form-urlencoded',
					'Cookie':cookie
				} 
		proxies = { 'http' : '222.134.134.250:8118'
				}     
		#response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(body))
		try:
			r = requests.post(url,headers=headers, data=body)
			#r=requests.post(url=url,headers=headers,params=urllib.parse.urlencode(body),proxies=proxies)
			#print (response)
			ddata = json.loads(r.text)
		except:
			#print ("EXCEPT")
			ddata = {'status':-1,'data':[]}
			return ddata
		else:
			return ddata
	 
	def getCookie(self) :
		url='http://api.gb6m.com/index/index.php?c=index&m=userOther&a=arcAdPlacePlatform'
		headers = {
			'User-Agent' : 'ZHIXIAO_A'
		}
		try:
			r = requests.get(url,headers=headers)
		except:
			return None
		else:
			return r.headers['Set-Cookie']

	def login(self, moblie, only, cookie):
		#print ("登录")
		url = 'http://api.gb6m.com/index/index.php?c=index&m=user&a=new_login'
		body = {'only': only, 'password': '123456', 'mobile':moblie, 'come_from':'zhixiao'}  
		data=self.visit(url, body, cookie)
		#print(data)
		return data
		
	def intoApp(self, moblieName,uid,mobile, cookie):
		url='http://api.gb6m.com/index/index.php?c=index&m=user&a=into_app'
		body={'mobile_name':moblieName,
				'uid' : uid,
				'login_type':"1",
				'mobile':mobile,
				'come_from':'zhixiao'
				}
		#print (body)
		data=self.visit(url,body, cookie)
		#print(data)
	def signDay(self, token, uid, cookie):
		#签到
		#print ("签到")
		url='http://api.gb6m.com/index/index.php?c=index&m=user&a=new_new_sign'
		body={'token':token,
				'uid' : uid
				}
		#print (body)
		data=self.visit(url,body, cookie)
		print("签到状态:%d"%data['status'])
		return data


	def getList(self, url, eTime, fTime, pageNum, xsign, ysign, token, uid, only, cookie):
		channels=[{'cid': '0', 'name': '推荐'}, {'cid': '1', 'name': '搞笑'}, {'cid': '2', 'name': '健康'}, {'cid': '3', 'name': '情感'}, {'cid': '6', 'name': '两性'}, {'cid': '7', 'name': '猎奇'}, {'cid': '8', 'name': '励志'}, {'cid': '9', 'name': '育儿'},{'cid': '10', 'name': '科技'}, {'cid': '11', 'name': '汽车'}, {'cid': '14', 'name': '职场'}, {'cid': '45', 'name': '风水'}, {'cid': '12', 'name': '星座'}, {'cid': '18', 'name': '娱乐'}, {'cid': '19', 'name': '八卦'}, {'cid': '26', 'name':'心理'}, {'cid': '32', 'name': '家居'}, {'cid': '34', 'name': '宠物'}, {'cid': '37', 'name': '社会'}, {'cid': '15', 'name': '美容'}, {'cid': '16', 'name': '化妆'}, {'cid': '17', 'name': '发型'}, {'cid': '30', 'name': '美食'}, {'cid': '20','name': '军事'}, {'cid': '39', 'name': '旅游'}, {'cid': '22', 'name': '佛学'}, {'cid': '23', 'name': '养生'}, {'cid': '24', 'name': '健身'}, {'cid': '25', 'name': '减肥'}, {'cid': '27', 'name': '段子'}, {'cid': '28', 'name': '糗事'}, {'cid': '44', 'name': '视频'}, {'cid': '31', 'name': '吃货'}, {'cid': '36', 'name': '房产'}, {'cid': '40', 'name': '创业'}]
		
		channel = random.randint(0,len(channels)-1)
		body={
			"end_time" : eTime,
			"xsign" : xsign,
			"first_time" : fTime,
			"action" : "下拉刷新",
			"only" : only,
			"token" : token,
			"cid" : channel,
			"uid" : uid,
			"from" : channels[channel]['name'],#励志(8) 猎奇(7)
			"ysign" : ysign,
			"type" : "1",
			"page" : pageNum,
		}
		#print (body)
		data=self.visit(url,body, cookie)
		#print (channels[channel]['name'])
		return data
		
	def readOne(self, token,uid,only, cookie):
		url="http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=article_list_new"
		xsign=random.randint(100,700)
		ysign=random.randint(100,700)
		pageNum=random.randint(1,3)

		fTime=int(time.time())
		eTime=fTime-24*60*100
		index=0
		while index==0: 
			dataBuf = self.getList(url, eTime, fTime, pageNum, xsign, ysign, token, uid, only, cookie)
			news=dataBuf['data']
			index=len(news)
			#print ("共%d条新闻"%index)
		if index>1:
			#print ("等一会......")
			time.sleep(random.randint(3,5))
			url='http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=readmoney'
			nid=news[0]['nid']
			body = {
				'uid':uid,
				'nid':nid
			}
			data=self.visit(url,body, cookie)
			print (data)
			time.sleep(3)
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=createMessage'
			body = {
				'content':'非常好非常棒棒',
				'sender':uid,
				'type':'1',
				'token':token,
				'nid':nid
			}
			data = self.visit(url, body, cookie)
			print("状态:%d"%data['status'])
			time.sleep(3)
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=comments'
			body = {
				'uid':uid,
				'page':'1',
				'aid':nid
			}
			data = self.visit(url, body, cookie)
			time.sleep(3)
			#print (data)
			rid = data['data'][0]['mrid']
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=thumbsUp'
			body={
				'uid':uid,
				'token':token,
				'nid':rid
			}
			data = self.visit(url, body, cookie)
			print("签到状态:%d"%data['status'])
			#print (data)
	def register(self, mobile, code, cookie):	
		url='http://api.gb6m.com/index/index.php'
		body={
			'c':'index',
			'm':'user',
			'a':'new_app_register'
		}
		proxies = {
			'http' : '222.134.134.250:8118'
		}   
		mdata={
			'mobile':mobile,
			'password':'123456',
			'come_from':'zhixiao',
			'code':code
		}
		headers={
			'User-Agent':'ZHIXIAO_A',
			'Host':'api.gb6m.com',
			'Cookie':cookie
		}
		
		r = requests.post(url, headers=headers, params=body, data=mdata)
		
		result = json.loads(r.text)
		
		print (result)
		return result

	def addUserMaster(self, uid, incode,cookie):
		url='http://api.gb6m.com/index/index.php?c=index&m=userIndex&a=addUserMaster'
		headers={
			'User-Agent':'ZHIXIAO_A',
			'Host':'api.gb6m.com',
			'Cookie':cookie
		}
		mdata={
			'uid':uid,
			'in_code':incode
		}
		r = requests.post(url, headers=headers, data=mdata)
		result=json.loads(r.text)
		#print (result)

	def visitList(self, token,uid,only, cookie):
		url="http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=article_list_new"
		xsign=random.randint(100,700)
		ysign=random.randint(100,700)
		pageNum=random.randint(1,3)

		fTime=int(time.time())
		eTime=fTime-24*60*100
		index=0
		while index==0: 
			dataBuf = self.getList(url, eTime, fTime, pageNum, xsign, ysign, token, uid, only, cookie)
			news=dataBuf['data']
			index=len(news)
		#print ("共%d条新闻"%index)
		sucCount=0
		if index>6:
			index=6
		for i in range(index):
			#print ("等一会......")
			time.sleep(random.randint(3,5))
			url='http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=readmoney'
			nid=news[i]['nid']
			body = {
				'uid':uid,
				'nid':nid
				}
			#print (body)
			#print ("第%d"%i)
			data=self.visit(url,body, cookie)
			#print (data)
			if data['status']==200:
				sucCount+=1
		return sucCount
		
	def readfile(self, path):
		fo = open(path)
		res=[]
		while 1:
			line = fo.readline()
			if not line:
				break
			res.append(line[0:len(line)-1])
		fo.close()
		return res
	def elog(self, path):
		file=open(path)
		str="%s.txt"%path
		file1=open(str, 'w+')
		while 1:
			line = file.readline()
			if not line:
				break
			if line.find('INFO') > 0:
				file1.write(line)
		file1.close()		
		file.close()
