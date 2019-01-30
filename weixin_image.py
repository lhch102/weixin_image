#!/usr/bin/env python3
import itchat
import math 
import PIL.Image as Image
import os

def login():
	#产生二维码
	itchat.auto_login(enableCmdQR=True,hotReload=True)
	friends = itchat.get_friends(update=True)
	return friends

def get_head_img(friends):
	# 创建image文件夹保存微信好友头像照片
	if not os.path.exists('images'):
		os.mkdir('images')
	for friend in friends:
		remarkName = friend['RemarkName']
		print(remarkName)
		# 根据用户名获取好友头像
		img = itchat.get_head_img(userName=friend['UserName'])
		# 保存好友头像
		fileImage = open('./images/' + str(remarkName) + ".jpg",'wb')
		fileImage.write(img)
		fileImage.close()

def make_all_img():
	all_image = os.listdir('images') # 获得头像列表
	each_size = int(math.sqrt(float(640*640)/len(all_image)))# 拼接头像大小
	lines = int(640/each_size) # 照片墙行数
	image = Image.new('RGBA',(640,640)) # 初始化Image对象，初始化大小
	x = 0
	y = 0
	file_dir = './images'
	for root, dirs, files in os.walk(file_dir):
		for file in files:  
			title = os.path.splitext(file)[0]
			try:
				if os.path.splitext(file)[1] == '.jpg':
					#打开头像
					img = Image.open('images' + '/' + title + '.jpg')
					# 重新设置大小
					img = img.resize((each_size,each_size),Image.ANTIALIAS)
					# 设置x,y坐标位置拼接头像
					image.paste(img,(x * each_size,y * each_size))
					# 下一张照片
					x += 1
					if x == lines:# 一行一行拼接
						x = 0 # 如果一行满了，设置x为0
						y += 1 # y+1进入下一行
			except Exception as err:
				print("错误")
	image.save('all.png')	 # 保存照片墙

def senf_image():
	#发送微信文件传输助手，手机可以查看
	itchat.send_image('all.png','filehelper')
def main():
	friends = login()
	get_head_img(friends)
	make_all_img()
	senf_image()

if __name__ == '__main__':
	main()
