from common import Util
from yima import *
from sys import argv
from userinfo import UserInfoService

uis = UserInfoService()
def run(master):
	#login
	print ('login yi ma......')
	token=loginYima()
	itemid='2730'
	cookie=''
	time.sleep(3)
	print(token)
	#get mobile
	print ('get mobile......')
	mobile=getMobile(token)
	print ("mobile:%s"%mobile)
	#get code
	print ('get code......')
	time.sleep(3)
	only = util.gen_imme()
	cookie, status = getCode(mobile, only)
	print ("status:%d"%status)
	if status==200:
		#get message
		print ('get sms......')
		time.sleep(3)
		code=getMessage(token, mobile, itemid)
	#register
	print ('register a count......')
	time.sleep(3)
	data = util.register(mobile, code, cookie)
	token1=data['data']['token']
	uid=data['data']['uid']
	#add a user info
	user_info = [(
			data['data']['uid'], data['data']['mobile'], data['data']['ip'], data['data']['level'],
			data['data']['invite_code'], data['data']['score'], data['data']['register_time'], 
			data['data']['total_read']
			)]
	uis.save(user_info)
	
	uid = data['data']['uid']
	user_flag = [(uid,)]
	#save_flag
	uis.save_flag(user_flag)
	#update flag
	uis.update_flag([(0, 0, uid)])
	print("save complete.....")
	incodes=['FbsP2d','fNpFYh','4T8pua','Wlemfv','TLc7gb']
	#add mater
	print ('add master......')
	time.sleep(3)
	util.addUserMaster(uid, incodes[master], cookie)
	#sign
	time.sleep(3)
	util.signDay(token1, uid, cookie)
	#read 
	time.sleep(3)
	util.readOne(token1,uid,only, cookie)
	#release 
	print ('release all number......')
	time.sleep(3)
	result=releaseAll(token)
	if result=="success":
		print (result)

master=int(argv[1])
util = Util()
run(master)




	



