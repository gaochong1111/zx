

from common import *

def run(mobile) :
	util = Util()
	print("账号:%s"%mobile)
	only=util.gen_imme()
	mobileNames=['KIW-TL00H','FRD-AL00','KIW-TL00','FRD-AL00H']
	cookie=util.getCookie()
	data = util.login(mobile, only, cookie)
	time.sleep(random.randint(1,3))
	token=data['data']['token']
	uid=data['data']['uid']
	mobile=data['data']['mobile']
	
	time.sleep(random.randint(1,3))
	util.intoApp(mobileNames[0],uid,mobile, cookie)
	time.sleep(random.randint(1,3))
	#签到
	util.signDay(token,uid, cookie)
	#get List
	time.sleep(random.randint(3,5))
	total1=0
	while total1<15:
			count=util.visitList(token,uid,only, cookie)
			total1+=count
			print ("read%d"%total1)
	



#main
#mobile = argv[1]
mobile='15503820160'
#end = int(argv[2])

run(mobile)

print ('main thread end!')
	



