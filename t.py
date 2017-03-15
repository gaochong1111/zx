from userinfo import UserInfoService
import time
from common import Util

import threading

#db = DBUtil('data/test.db', 'userinfo', True)

def test():
	uiService = UserInfoService()


	data = {
			'status': 200, 'message': '登录成功', 
			'data': {
				'uid': '17290718', 'username': '131****1040', 
				'sex': '1', 'mobile': '13115011040', 
				'ip': '42.239.131.183', 'level': '3', 
				'avatar': 'http://images.52cgs.com/user/default.png', 
				'invite_code': 'rA5aWE', 'score': '10136', 
				'register_time': '1486107615', 
				'token': 'df21c976ea4c14eb16bc6827545d27f9', 
				'mobile_code_status': '1', 'total_read': '795'
			}
		}

	data1 = [(
		data['data']['uid'], data['data']['mobile'], data['data']['ip'], data['data']['level'],
		data['data']['invite_code'], data['data']['score'], data['data']['register_time'], 
		data['data']['total_read']
		)]
	#test save
	uiService.save(data1)

	uid = data['data']['uid']
	data2 = [(uid,)]
	#test save_flag
	uiService.save_flag(data2)

	data3 = [(uid, int(time.time()), 3)]
	#test save_read_record
	uiService.save_read_record(data3)
	
def test_fetch():
	'''测试 从数据库取数据'''
	
	uiService = UserInfoService()
	#test fetch_all
	#uiService.get_all()
	
	#uiService.update_all_flag()
	
	#test get_all_user_read
	print("#"*80)
	res = uiService.get_all_user_read()
	for r in res:
		print(r)
		
	#test get_all_user_flag
	print("#"*80)
	res = uiService.get_all_user_flag(1)
	for r in res:
		print(r)
	
	#test fetch_one
	#uid = 17290718
	#uiService.get_one(uid)
	#test get_one_user
	#user_info = uiService.get_one_user()
	#print(user_info)
	
def test_update():
	uiService = UserInfoService()
	data1 = [(2, 0, 1000, 17290718)]
	#test update
	uiService.update(data1)
	
	data2 = [(1, 1, 17290718)]
	#test update_flag
	uiService.update_flag(data2)
	
	
def test_time():
	#当前时间毫秒数
	time_ms = int(time.time())
	time_local = time.localtime(time_ms)
	time_format = "%Y-%m-%d"
	time_str = time.strftime(time_format, time_local)
	time_local = time.strptime(time_str, time_format)
	time_ms = int(time.mktime(time_local))
	print("今日00:00对应毫秒:{}".format(time_ms))
	
def test_util():
	ut = Util()
	cookie = ut.getCookie()
	if cookie:
		print("cookie:{}".format(cookie))
	else:
		print("None")
		
class TestThread(threading.Thread):
	'''测试多线程'''
	
	def __init__(self, i):
		threading.Thread.__init__(self)
		self.name = "Thread-{}".format(i)
	
	def run(self):
		global mutex
		if mutex.acquire():
			self.increment()
			mutex.release()
		print ("{} : {}".format(self.name, count))
	
	def increment(self):
		global count
		count += 1
		time.sleep(1)
		
		
		
		
def test_threading():
	thread_list = []
	for i in range(100):
		t = TestThread(i)
		thread_list.append(t)
	
	for t in thread_list:
		t.start()
	
	for t in thread_list:
		t.join()
	
	
	
	
mutex = threading.Lock()
count = 0
if "__main__" == __name__:
	test_time()
