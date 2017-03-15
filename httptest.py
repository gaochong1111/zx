
import threading
from common import *
from sys import argv
from userinfo import UserInfoService
		
		#get List
		
#http://api.gb6m.com/index/index.php?c=index&m=user&a=new_login
#Login
lock = threading.Lock()
uis = UserInfoService()

class MyThread(threading.Thread):
	'''
		定义自己的线程类,重写run函数
	'''
	
	def __init__(self, id):
		'''初始化线程信息'''
		threading.Thread.__init__(self)
		self.name = "Thread-{}".format(id)
		
	def run(self) :
		#声明共享资源和锁
		global lock, uis
		#工具类对象
		myUtil = Util()
		mobileNames=['KIW-TL00H','FRD-AL00','KIW-TL00','FRD-AL00H']
		for i in range(5):
			print("{} : {} times".format(self.name, i))
			#1. get one user
			if lock.acquire():
				user = uis.get_one_user()
				lock.release()
				
			if user:
				#get mobile
				mobile = user[1]
				uid = user[0]
				#update flag
				if lock.acquire():
					read_flag = [(1, 1, uid)]
					uis.update_flag(read_flag)
					lock.release()
				
				#generate a only code
				only=myUtil.gen_imme()
				#get cookie
				cookie = myUtil.getCookie()
				if cookie:
					time.sleep(random.randint(1,3))
					#login 
					data = myUtil.login(mobile, only, cookie)
					if data['status'] == 200:
						token = data['data']['token']
						level = data['data']['level']
						score = data['data']['score']
						total_read = data['data']['total_read']
						#update userinfo
						
						if lock.acquire():
							user_info = [(level, score, total_read, uid)]
							uis.update(user_info)
							lock.release()
						
						#sign
						data = myUtil.signDay(token, uid, cookie)
						time.sleep(random.randint(1,3))
						#read list
						THRESHOLD = 18
						total = 0
						while total < THRESHOLD:
							count = myUtil.visitList(token, uid, only, cookie)
							if count > 0:
								if lock.acquire():
									read_record = [(uid, int(time.time()), count)]
									#save_read_record
									uis.save_read_record(read_record)
									lock.release()
								total += count
								print("{} -- {} times -- total : {}".format(self.name, i, total))
						#update flag
						if lock.acquire():
							read_flag = [(2, 1, uid)]
							uis.update_flag(read_flag)
							lock.release()
				else:
					print("Cookie is None.")
			else:
				print("No Users")
				break
							
#main
def main():
	thread_list = []    #线程存放列表  
	ut = Util()
	THREAD_NUM = 5
	for i in range(0, THREAD_NUM):
		t = MyThread(i)
		t.setDaemon(True)
		thread_list.append(t)

	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

def init_data():
	ut = Util()
	#get all mobiles 
	mobile_list = []
	for i in range(8):
		path = "mobile/mobiles{}.txt".format(i)
		mobiles = ut.readfile(path)
		mobile_list.extend(mobiles)
	#print ("mobile_list length: {}".format(len(mobile_list)))
	#get from database
	all_user_info = uis.get_all()
	for user_info in all_user_info:
		mobile_list.remove(user_info[1])
	#print ("mobile_list length: {}".format(len(mobile_list)))
	
	for mobile in mobile_list:
		only = ut.gen_imme()
		cookie = ut.getCookie()
		if cookie:
			time.sleep(1)
			#login get user info
			data = ut.login(mobile, only, cookie)
			user_info = [(
				data['data']['uid'], data['data']['mobile'], data['data']['ip'], data['data']['level'],
				data['data']['invite_code'], data['data']['score'], data['data']['register_time'], 
				data['data']['total_read']
				)]
			#save user info
			uis.save(user_info)

			uid = data['data']['uid']
			user_flag = [(uid,)]
			#save_flag
			uis.save_flag(user_flag)
		else:
			print ("None, mobile is {}".format(mobile))
			break
			

if "__main__" == __name__:
	main()
	#init_data()
	print ('main thread end!')
	



