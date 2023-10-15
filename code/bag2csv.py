#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#creator：huxianhe
#name:批量读取rosbag并写成csv文件的脚本
#create time:2019-05-31 15:14:01

import rosbag, sys, csv
import time
import string
import os #用os命令创建文件夹
import shutil #用于文件的复制管理等操作

#检验输入数量: 1 or 2
if (len(sys.argv) > 2):
	print ("无效数量:   " + str(len(sys.argv)))
	print ("应该包含两项: 'bag2csv.py' and 'bagName'")
	sys.exit(1)
elif (len(sys.argv) == 2):
	listOfBagFiles = [sys.argv[1]]
	print ("读取rosbag文件: " + str(listOfBagFiles[0]))
	numberOfFiles='1'
elif (len(sys.argv) == 1):
	listOfBagFiles = [f for f in os.listdir(".") if f[-4:] == ".bag"]	#读取当前文件夹下的rosbag文件名list
	numberOfFiles = str(len(listOfBagFiles))
	print ("读取总计 " + numberOfFiles + " 个rosbag文件在当前文件夹: \n")
	for f in listOfBagFiles:
		print (f)
	#time.sleep(10)
else:
	print (": " + str(sys.argv))	#不应该出现的情况
	sys.exit(1)

count = 0
for bagFile in listOfBagFiles:
	count += 1
	print ("读取总计 " + str(count) + " 个文件  " + numberOfFiles + ": " + bagFile)
	bag = rosbag.Bag(bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename


	#创建一个新的文件夹
	folder = bagName.rstrip(".bag")
	try:	
		os.makedirs(folder)
	except:
		pass
	# shutil.copyfile(bagName, folder + '/' + bagName)  #实现复制操作


	#得到rosbag的所有主题
	listOfTopics = []
	type, topic = bag.get_type_and_topic_info()
	listOfTopics = list(topic)

	for topicName in listOfTopics:
		#为每个主题创建一份csv
		print (topicName)
		filename = folder + '_' + topicName.replace( '/', '_') + '.csv'
		with open(filename, 'w+') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			firstIteration = True	#使用标题行
			for subtopic, msg, t in bag.read_messages(topicName):	# 把每一个topicName的数据都弄下来
				# 都是这个格式"Name: value\n"
				# 把数据放在一个二维list里
				# print msg
				msgString = str(msg)
				msgList = msgString.split('\n')
				instantaneousListOfData = []
				for nameValuePair in msgList:
					splitPair = nameValuePair.split(':')
					for i in range(len(splitPair)):
						print (splitPair[i])
						#splitPair[i] = splitPair.strip(splitPair[i])
						#这里后面可能会改一下
					instantaneousListOfData.append(splitPair)
				#从每队的第一行元素开始写第一行
				if firstIteration:	# 头部
					headers = ["rosbagTimestamp"]	#第一列
					for pair in instantaneousListOfData:
						headers.append(pair[0])
					filewriter.writerow(headers)
					firstIteration = False
				# 把每列元素写进文本里
				values = [str(t)]	#第一列元素一定要有时间戳
				for pair in instantaneousListOfData:
					if len(pair)>1:
						values.append(pair[1])
					else:
						values.append('')
				filewriter.writerow(values)
	bag.close()
print ("Done reading all " + numberOfFiles + " bag files.")