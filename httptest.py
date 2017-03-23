
import threading
from common import ZX
from sys import argv
from userinfo import UserInfoService
import time
import random	
	
lock = threading.Lock() #mutex lock
uis = UserInfoService()

class MyThread(threading.Thread):
	'''
		定义自己的线程类,重写run函数
	'''
	
	def __init__(self, id, i_num):
		'''初始化线程信息'''
		threading.Thread.__init__(self)
		self.name = "Thread-{}".format(id)
		self.ITER_NUM = i_num
		
	def run(self) :
		#声明共享资源和锁
		global lock, uis
		#工具类对象
		for i in range(self.ITER_NUM):
			#print("{} : {} times".format(self.name, i))
			#1. get one user
			if lock.acquire():
				print("{} : {} times in critical region".format(self.name, i))
				# read a user and update flag
				user = uis.get_one_user()
				if user:
					read_flag = [(1, 1, user[0])]
					uis.update_flag(read_flag)
				lock.release()
				
			if user:
				#2. get mobile and create zx 
				mobile = user[1]
				zx = ZX(mobile)
				uid = user[0]
				if zx.cookie:
					time.sleep(random.randint(1,3))
					#3. login 
					info = zx.login()
					if info:
						#print("{} get mobile:{}  get uid:{} zx.uid:{}".format(self.name, mobile, uid, zx.uid))
						#4. update flag
						
						level, score, total_read = info
						#5. update userinfo
						if lock.acquire():
							user_info = [(level, score, total_read, uid)]
							uis.update(user_info)
							lock.release()
						
						#6. sign
						data = zx.sign_daily()
						time.sleep(random.randint(1,3))
						#7. read list
						THRESHOLD = 18
						total = 0 # total read times
						read_zero_num = 0 #the count of read valid times is zero
						while total < THRESHOLD and read_zero_num < 5:
							count = zx.visit_list()
							if count > 0:
								if lock.acquire():
									read_record = [(zx.uid, int(time.time()), count)]
									#8. save_read_record
									uis.save_read_record(read_record)
									lock.release()
								total += count
								print("{} ---- {} times -- total : {}".format(self.name, i, total))
							else:
								read_zero_num += 1
						#9. update flag
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
def main(t_num=7, i_num=5):
	thread_list = []    #线程存放列表  
	THREAD_NUM = t_num
	for i in range(0, THREAD_NUM):
		t = MyThread(i, i_num)
		t.setDaemon(True)
		thread_list.append(t)

	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()
		
if "__main__" == __name__:
	if len(argv)>1:
		main(int(argv[1]), int(argv[2]))
	else:
		main()
	#test_obj()
	#init_data()
	print ('main thread end!')
	



