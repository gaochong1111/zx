from common import ZX
from yima import YIMA
from sys import argv
from userinfo import UserInfoService
import time
import random

uis = UserInfoService()
def run(master):
	itemid='2730'
	ym = YIMA(itemid)
	#1. login yima
	print ('login yi ma......')
	ym.login_yima()
	time.sleep(3)
	#ym.release_all()
	#2. get mobile and create zx
	print ('get mobile......')
	mobile=ym.get_mobile()
	zx = ZX(mobile)
	print ("mobile:%s"%mobile)
	#3. get sms code
	print ('get code......')
	time.sleep(3)
	status = zx.get_sms_code()
	print ("status:{}".format(status))
	if status==200:
		#4. get message
		print ('get sms......')
		time.sleep(3)
		code=ym.get_code()
	else:
		print("expection..")
		return None
		
	#5. register
	print ('register a count......')
	time.sleep(3)
	data = zx.register(code)
	#6. add a user info
	uis.save(zx.user_info)
	user_flag = [(zx.uid,)]
	#7. save_flag
	uis.save_flag(user_flag)
	#8. update flag
	uis.update_flag([(0, 0, zx.uid)])
	print("save complete.....")
	incodes=['FbsP2d', 'fNpFYh', '4T8pua', 'Wlemfv', 'TLc7gb']
	#9. add mater
	print ('add master......')
	time.sleep(3)
	zx.add_user_master(incodes[master])
	#10. sign
	time.sleep(3)
	zx.sign_daily()
	#read 
	time.sleep(3)
	zx.read_one()
	#release 
	print ('release all number......')
	time.sleep(3)
	result=ym.release_all()
	if result=="success":
		print (result)

master=int(argv[1])
run(master)




	



