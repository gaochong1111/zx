import random
import requests
import json
import time
import math
import requests

class ZX(object):
	delay = 8
	'''
		util class
	'''
	def __init__(self, mobile):
		self.mobile = mobile
		self.cookie=self.get_cookie()
		#self.cookie = self.get_cookie()
		self.only = self.gen_imme()
		
		#print("only:{}".format(self.only))
	
	def luhn_check(self, num):
		'''
			check the num
		'''
		digits = [int(x) for x in reversed(str(num))]
		check_sum = sum(digits[1::2]) + sum((dig//10 + dig%10) for dig in [2*el for el in digits[::2]])
		return (10-check_sum%10)%10
		
	def gen_imme(self):
		'''
			generate a imme
		'''
		TAC='867922'
		FAC='02'
		SNR=565583
		imme=TAC+FAC+str(SNR+random.randint(1,1000))
		return (imme+str(self.luhn_check(imme)))
		
	
	
	def visit(self, url, body):
		'''
			visit url
		'''
		headers = { 'User-Agent' : 'ZHIXIAO_A',
					'Content-type': 'application/x-www-form-urlencoded',
					'Cookie':self.cookie
		} 
		try:
			r = requests.post(url,headers=headers, data=body)
			ddata = json.loads(r.text)
		except:
			#ddata = {'status':-1,'data':[]}
			
			print("Except, sleep: {}".format(self.delay))
			time.sleep(self.delay)
			self.delay *= 2
			return self.visit(url, body)
		else:
			self.delay = 8
			return ddata
	 
	def get_cookie(self) :
		'''
			get cookie
		'''
		url='http://api.gb6m.com/index/index.php?c=index&m=userOther&a=arcAdPlacePlatform'
		headers = {
			'User-Agent' : 'ZHIXIAO_A'
		}
		try:
			r = requests.get(url,headers=headers)
		except:
			print("Except, sleep: {}".format(self.delay))
			time.sleep(self.delay)
			self.delay *= 2
			return self.get_cookie()
		else:
			self.delay = 8
			cookie = r.headers['Set-Cookie']
			return cookie

	def login(self):
		'''
			login 
		'''
		#print ("登录")
		url = 'http://api.gb6m.com/index/index.php?c=index&m=user&a=new_login'
		body = {
			'only': self.only, 
			'password': '123456', 
			'mobile': self.mobile, 
			'come_from':'zhixiao'
		}  
		data=self.visit(url, body)
		if data['status'] == 200:
			self.uid = data['data']['uid']
			self.token = data['data']['token']
			level = data['data']['level']
			score = data['data']['score']
			total_read = data['data']['total_read']
			self.user_info = [(
				data['data']['uid'], data['data']['mobile'], data['data']['ip'], data['data']['level'],
				data['data']['invite_code'], data['data']['score'], data['data']['register_time'], 
				data['data']['total_read']
			)]
			return level, score, total_read
		else:
			return None
		
	def sign_daily(self):
		'''
			singn daily
		'''
		#签到
		#print ("签到")
		url='http://api.gb6m.com/index/index.php?c=index&m=user&a=new_new_sign'
		body={
			'token':self.token,
			'uid' : self.uid
		}
		#print (body)
		data=self.visit(url,body)
		#print(data)
		print("mobile:{} 签到状态:{}".format(self.mobile, data['status']))
		return data

	def visit_list(self):
		'''
			visit a list
			return:
				read count
		'''
		url="http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=article_list_new"
		index=0
		while index==0: 
			temp_data = self.get_list(url)
			news_list=temp_data['data']
			index=len(news_list)
		#print ("共%d条新闻"%index)
		sucCount=0
		if index>6:
			index=6
		for i in range(index):
			#print ("等一会......")
			time.sleep(random.randint(3,5))
			url='http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=readmoney'
			nid=news_list[i]['nid']
			body = {
				'uid':self.uid,
				'nid':nid
			}
			#print (body)
			data=self.visit(url,body)
			#print (data)
			if data['status']==200:
				sucCount+=1
		return sucCount

	def get_list(self, url):
		'''
			get content list 
		'''
		channels=[{'cid': '0', 'name': '推荐'}, {'cid': '1', 'name': '搞笑'}, {'cid': '2', 'name': '健康'}, {'cid': '3', 'name': '情感'}, {'cid': '6', 'name': '两性'}, {'cid': '7', 'name': '猎奇'}, {'cid': '8', 'name': '励志'}, {'cid': '9', 'name': '育儿'},{'cid': '10', 'name': '科技'}, {'cid': '11', 'name': '汽车'}, {'cid': '14', 'name': '职场'}, {'cid': '45', 'name': '风水'}, {'cid': '12', 'name': '星座'}, {'cid': '18', 'name': '娱乐'}, {'cid': '19', 'name': '八卦'}, {'cid': '26', 'name':'心理'}, {'cid': '32', 'name': '家居'}, {'cid': '34', 'name': '宠物'}, {'cid': '37', 'name': '社会'}, {'cid': '15', 'name': '美容'}, {'cid': '16', 'name': '化妆'}, {'cid': '17', 'name': '发型'}, {'cid': '30', 'name': '美食'}, {'cid': '20','name': '军事'}, {'cid': '39', 'name': '旅游'}, {'cid': '22', 'name': '佛学'}, {'cid': '23', 'name': '养生'}, {'cid': '24', 'name': '健身'}, {'cid': '25', 'name': '减肥'}, {'cid': '27', 'name': '段子'}, {'cid': '28', 'name': '糗事'}, {'cid': '44', 'name': '视频'}, {'cid': '31', 'name': '吃货'}, {'cid': '36', 'name': '房产'}, {'cid': '40', 'name': '创业'}]
		fTime=int(time.time())
		eTime=fTime-24*60*100
		xsign=random.randint(100,700)
		ysign=random.randint(100,700)
		
		channel = random.randint(0,len(channels)-1)
		
		body={
			"end_time" : eTime,
			"xsign" : xsign,
			"first_time" : fTime,
			"action" : "下拉刷新",
			"only" : self.only,
			"token" : self.token,
			"cid" : channel,
			"uid" : self.uid,
			"from" : channels[channel]['name'],#励志(8) 猎奇(7)
			"ysign" : ysign,
			"type" : "1",
			"page" : 1,
		}
		#print (body)
		data=self.visit(url,body)
		return data
		
	
	def get_sms_code(self):
		'''
			get sms code
			return 
				status
		'''
		#get cookie
		url='http://api.gb6m.com/index/index.php?c=index&m=user&a=do_app'
		mdata = {
			'only':self.only
		}
		r=requests.post(url, data=mdata)
		#print (r.headers['Set-Cookie'])
		self.cookie=r.headers['Set-Cookie']
		result = json.loads(r.text)
		print(result)
		mdata = {
			'only':self.only
		}
		
		r = requests.post(url, data=mdata)
		self.cookie = r.headers['Set-Cookie']
		time.sleep(5)
		url='http://api.gb6m.com/index/index.php'
		body={
			'c':'index',
			'm':'user',
			'a':'send_mobile_code'
		}
		mdata={
			'mobile':self.mobile
		}
		headers={
			'User-Agent':'ZHIXIAO_A',
			'Host':'api.gb6m.com',
			'Cookie':self.cookie
		}
		r = requests.post(url, headers=headers, params=body, data=mdata)
		
		result = json.loads(r.text)
		print(result)
		status = result['status']
		return status
		
	def register(self, code):
		'''
			registe a user
		'''
		
		url='http://api.gb6m.com/index/index.php'
		
		body={
			'c':'index',
			'm':'user',
			'a':'new_app_register'
		}
		mdata={
			'mobile':self.mobile,
			'password':'123456',
			'come_from':'zhixiao',
			'code':code
		}
		headers={
			'User-Agent':'ZHIXIAO_A',
			'Host':'api.gb6m.com',
			'Cookie':self.cookie
		}
		
		r = requests.post(url, headers=headers, 
				params=body, data=mdata)
		
		data = json.loads(r.text)
		print (data)
		self.uid = data['data']['uid']
		self.token = data['data']['token']
		self.user_info = [(
			data['data']['uid'], data['data']['mobile'], data['data']['ip'], data['data']['level'],
			data['data']['invite_code'], data['data']['score'], data['data']['register_time'], 
			data['data']['total_read']
		)]
		return data

	def read_one(self):
		'''
			read one news and comments
		'''
		#1. get list
		url="http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=article_list_new"
		index=0
		while index==0: 
			dataBuf = self.get_list(url)
			news=dataBuf['data']
			index=len(news)
		if index>1:
			#2. read one
			time.sleep(random.randint(3,5))
			url='http://api.gb6m.com/index/index.php?c=index&m=userArticle&a=readmoney'
			nid=news[0]['nid']
			body = {
				'uid':self.uid,
				'nid':nid
			}
			data=self.visit(url,body)
			print (data)
			time.sleep(3)
			#3. comment
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=createMessage'
			body = {
				'content':'非常好非常棒棒',
				'sender':self.uid,
				'type':'1',
				'token':self.token,
				'nid':nid
			}
			data = self.visit(url, body)
			print("状态:%d"%data['status'])
			time.sleep(3)
			#4. get comment list
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=comments'
			body = {
				'uid':self.uid,
				'page':'1',
				'aid':nid
			}
			data = self.visit(url, body)
			time.sleep(3)
			rid = data['data'][0]['mrid']
			#5. thumbs up
			url = 'http://api.gb6m.com/index/index.php?c=index&m=notify&a=thumbsUp'
			body={
				'uid':self.uid,
				'token':self.token,
				'nid':rid
			}
			data = self.visit(url, body)
			print("签到状态:%d"%data['status'])
			#print (data)
			
	def add_user_master(self, incode):
		'''
			add master
		'''
		url='http://api.gb6m.com/index/index.php?c=index&m=userIndex&a=addUserMaster'
		headers={
			'User-Agent':'ZHIXIAO_A',
			'Host':'api.gb6m.com',
			'Cookie':self.cookie
		}
		mdata={
			'uid':self.uid,
			'in_code':incode
		}
		r = requests.post(url, headers=headers, data=mdata)
		result=json.loads(r.text)
		#print (result)

if "__main__" == __name__:
	print("common")