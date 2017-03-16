from userinfo import UserInfoService
from common import *


uis = UserInfoService()
myUtil = Util()

def readRegUser():
	'''
		完成注册User的任务
	'''
	print("Register User.")
	#get user
	users = uis.get_register()
	for user in users:
		#get mobile
		mobile = user[1]
		uid = user[0]
		
		#generate a only code
		only=myUtil.gen_imme()
		#get cookie
		cookie = myUtil.getCookie()
		if cookie:
			time.sleep(random.randint(1,3))
			#login 
			data = myUtil.login(mobile, only, cookie)
			token = data['data']['token']
			if data['status'] == 200:
				#read list
				THRESHOLD = 15
				total = 0
				while total < THRESHOLD:
					count = myUtil.visitList(token, uid, only, cookie)
					if count > 0:
						read_record = [(uid, int(time.time()), count)]
						#save_read_record
						uis.save_read_record(read_record)
						total += count
						print("mobile: {}  -- total : {}".format(mobile, total))
				#update flag
				read_flag = [(2, 1, uid)]
				uis.update_flag(read_flag)
		else:
			print("Cookie is None.")
		

def readReadingUser():
	'''
		完成一个User的任务
	'''
	print("Reading User.")
	#get user
	users = uis.get_all_reading_user()
	for user in users:
		#get mobile
		mobile = user[1]
		uid = user[0]
		read_count = uis.get_user_read_count(uid)
		#generate a only code
		only=myUtil.gen_imme()
		#get cookie
		cookie = myUtil.getCookie()
		if cookie:
			time.sleep(random.randint(1,3))
			#login 
			data = myUtil.login(mobile, only, cookie)
			token = data['data']['token']
			if data['status'] == 200:
				time.sleep(random.randint(1,3))
				#sign
				data = myUtil.signDay(token, uid, cookie)
				time.sleep(random.randint(1,3))
				#read list
				THRESHOLD = 18 - read_count
				total = 0
				while total < THRESHOLD:
					count = myUtil.visitList(token, uid, only, cookie)
					if count > 0:
						read_record = [(uid, int(time.time()), count)]
						#save_read_record
						uis.save_read_record(read_record)
						total += count
						print("mobile: {}  -- total : {}".format(mobile, total))
				#update flag
				read_flag = [(2, 1, uid)]
				uis.update_flag(read_flag)
		else:
			print("Cookie is None.")
		
	
if "__main__" == __name__:
	readRegUser()
	readReadingUser()
	print ("read over...")

