from userinfo import UserInfoService
from common import ZX
import time
import random

uis = UserInfoService()

def read_reg_user():
	'''
		完成注册User的任务
	'''
	print("Register User.")
	#1. get user
	users = uis.get_register()
	read_users(users)
	
def read_reading_user():
	'''
		完成一个User的任务
	'''
	print("Reading User.")
	#get user
	users = uis.get_all_reading_user()
	read_users(users)
	
def read_users(users):
	for user in users:
		if user:
			#2. get mobile and create zx 
			mobile = user[1]
			zx = ZX(mobile)
			
			if zx.cookie:
				time.sleep(random.randint(1,3))
				#login 
				data = zx.login()
				read_count = uis.get_user_read_count(zx.uid)
				if data:
					#read list
					THRESHOLD = 15 - read_count
					total = 0
					while total < THRESHOLD:
						count = zx.visit_list()
						if count > 0:
							read_record = [(zx.uid, int(time.time()), count)]
							#save_read_record
							uis.save_read_record(read_record)
							total += count
							print("mobile: {}  -- total : {}".format(mobile, total))
					#update flag
					read_flag = [(2, 1, zx.uid)]
					uis.update_flag(read_flag)
			else:
				print("Cookie is None.")


if "__main__" == __name__:
	read_reg_user()
	read_reading_user()
	print ("read over...")

