

from common import ZX
import time
import random

def run(mobile) :
	zx = ZX(mobile)
	print("账号:%s"%mobile)
	data = zx.login()
	time.sleep(random.randint(1,3))
	#签到
	zx.sign_daily()
	#get List
	time.sleep(random.randint(3,5))
	total=0
	total = 0 # total read times
	read_zero_num = 0 #the count of read valid times is zero
	THRESHOLD = 15
	while total < THRESHOLD and read_zero_num < 5:
		count = zx.visit_list()
		if count > 0:
			total += count
			print("read_zero_num: {}  total: {}".format(read_zero_num, total))
		else:
			read_zero_num += 1

#main
#mobile = argv[1]
mobile='15503820160'
#end = int(argv[2])

run(mobile)

print ('main thread end!')
	



