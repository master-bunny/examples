# coding: utf-8

from os import getenv
import requests
import json
import sys
from json import dumps
from datetime import datetime
import base64
from datetime import timedelta
from collections import Counter 
import time
from bitrix24 import *
import pymysql
import pymssql
from io import BytesIO
from calendar import timegm
import math
from PIL import Image
import os
import math
import ssl
import re
import ciso8601
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler)
from pytz import timezone
#DATE_TIME FORMATER
fmt = "%d-%m-%Y %H:%M"
now_utc = datetime.now(timezone('UTC'))
now_moscau = now_utc.astimezone(timezone('Europe/Moscow'))
currenttime2 = now_moscau.strftime(fmt)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#PAIN IN ARSE O'CLOCK BOI
currenttime = datetime.today() + timedelta(days=1)
doorphonedeadline = datetime.today() + timedelta(days=7)
currenttime = currenttime.strftime('%Y%m%d')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
no = "/"	 #just string formatting shit
space = "  " #just string formatting shit
end = ")" #just string formatting shit	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#SETUP DAT-A-BASE CONNECTION
server = "SRV_IP"
user = "USER"
password = "PASS"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#SETUP VARIABLES BOI
#text = "(№	 93459)	 Тестовая заявка, пожалуйста не делайте с ней ничего"
bot = telegram.Bot('tlg_token')
animation = "|/-\\"
long = "[Остальной текст в заметке задачи]"
mark = "nope"
alert = "Обработка заявок FO"
i=0
delimeter = "|"
print(doorphonedeadline)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#CREATE BITRIX DAT-A-BASE CONNECTOR
conn = pymssql.connect(server, user, password, "CBase_FreshOffice")
connection = pymysql.connect(host='localhost',
							user='user',
							password='pass',
							db='bitrix_storage',
							charset='utf8',
							use_unicode = True,
							cursorclass=pymysql.cursors.DictCursor
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Functions here for non-spagethy code
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#BITRIX CLASS BOI
class bitrix:
	bx24 = Bitrix24('btx24_webhook')
	def uid(str):
		try:
			btx_tl_user = {"telegram_nickname":"btx24userid"}
			return btx_tl_user[str]
		except KeyError:
			return 74

	def create(title, discriptor, currenttime): #Create new task with classification
		status = 0
		catch_dp = ['домофон', 'домофона', 'домофо', 'омофо', 'д/ф', 'дф', 'абонентского', 'абонент'] #search for doorphone tasks
		catch_it = ['принтер', 'запрограммировать', 'принтеров', 'сканеров', 'сканер', 'почта', 'смс', 'сообщение',	'запрограмировать', 'запраграммировать', 'запраграмировать', 'брелок', 'брелка', 'брелока', 'компьютер', 'компутер', 'экран', 'завис', 'база', 'список', 'автомобиль', 'автомобиля', 'автомобилей', 'авто', 'машин', 'машина', 'машину', 'свет', 'интернет', 'печать', 'сеть'] #search for it tasks
		string = title.lower()
		string = title.replace("/", " ")
		string = string.replace("(", "")
		string = string.replace(")", "")
		string = string.replace(".", " ")
		string = string.replace(",", " ")
		string = string.split(" ")
		#print(string)
		if any(x in string for x in catch_dp):
			status = 1
			print('doorphone routine')
			try:
				rest = bitrix.bx24.callMethod('tasks.task.add', fields={'TITLE': title, 'RESPONSIBLE_ID': 158, 'DESCRIPTION':  discriptor, 'DEADLINE': doorphonedeadline, 'TAGS': ('цук', 'домофония'), 'GROUP_ID': 106, 'START_DATE_PLAN': currenttime, 'ACCOMPLICES': (112, 112), 'AUDITORS': (16, 28, 54) })
				task = rest['task']['id']
				print('doorphone routine')
				return task
				print(task)
			except BitrixError as message:
					return message
		if any(x in string for x in catch_it):
			status = 1
			print('it routine')
			try:
				rest = bitrix.bx24.callMethod('tasks.task.add', fields={'TITLE': title, 'RESPONSIBLE_ID': 64, 'DESCRIPTION':  discriptor, 'DEADLINE': doorphonedeadline, 'TAGS': ('цук', 'ИТ'), 'GROUP_ID': 110, 'START_DATE_PLAN': currenttime, 'ACCOMPLICES': (28, 74, 18), 'AUDITORS': (16, 16) })
				task = rest['task']['id']
				print('it routine')
				return task
				print(task)
			except BitrixError as message:
					return message
		else:	#doorphone task not found
			print('regular routine')
			try:
				rest = bitrix.bx24.callMethod('tasks.task.add', fields={'TITLE': title, 'RESPONSIBLE_ID': 62, 'DESCRIPTION':  discriptor, 'TAGS': ('цук', 'диспетчер', 'бд'), 'GROUP_ID': 68, 'START_DATE_PLAN': currenttime, 'ACCOMPLICES': (90, 104, 88, 114, 158), 'AUDITORS': (28, 28) })
				task = rest['task']['id']
				print('regular routine')
				return task
			except BitrixError as message:
				return message
	def check(bid):	 #Check task status with id
		try:
			rest = bitrix.bx24.callMethod('tasks.task.get', taskId=bid)
			#status 2 = pending task
			#status 5 = finished task
			#status 6 = delayed task
			user = rest['task']['responsible']['name']
			return user
		except BitrixError as message:
			return 'В битриксе не найдена'	
		except TypeError as message:
			return 'задача уничтожена, пользователь отсутствует'	
	def get_comm(bid):	 #Check task status with id
		try:
			rest = bitrix.bx24.callMethod('task.commentitem.getlist', taskId=bid)
			#status 2 = pending task
			#status 5 = finished task
			#status 6 = delayed task
			return rest
		except BitrixError as message:
			return 0
	def get_group():	 #get task by group id
		try:
			#rest = bitrix.bx24.callMethod('tasks.task.list', filter={'TAG':'selena'}, select=['ID','RESPONSIBLE_ID'])
			rest = bitrix.bx24.callMethod('tasks.task.list', filter={'GROUP_ID': '68', 'REAL_STATUS':'2', 'RESPONSIBLE_ID':'86'})
			#status 2 = pending task
			#status 5 = finished task
			#status 6 = delayed task
			return rest
		except BitrixError as message:
			return 0	
	def get_name(str):	 #get task by group id
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * FROM names WHERE human_name = %s"
				val = (str)
				cursor.execute(sql, val)
				connection.commit()		
				t = cursor.fetchall()
				#print(t)
				for row in t:
					print(row['long_name'])
					rest = bitrix.bx24.callMethod('tasks.task.list', filter={'TITLE':'%' + row['long_name'] + '%', 'GROUP_ID': '68', 'REAL_STATUS':'2'}, select=['ID','RESPONSIBLE_ID'])
					#print(rest)
					#print(len(rest['tasks']))
					#try:
					if len(rest['tasks']) <= 0:
						print('0')
					else:
						print(rest)
						return rest
					#except TypeError as message:
					#	print('type error')
					#status 2 = pending task
					#status 5 = finished task
					#status 6 = delayed task
					#print(rest)
					#return rest
		except BitrixError as message:
			return 0
	def name_translate(str):	 #get task by group id
		try:
			with connection.cursor() as cursor:
				str = str.split(" ")
				str = str[0]
				print(str)
				sql = "SELECT system_name,human_name FROM names WHERE long_name LIKE %s"
				val = ('%' + str + '%')
				cursor.execute(sql, val)
				connection.commit()		
				t = cursor.fetchone()
				return t
		except BitrixError as message:
			return 0
	def comment_get(id): #Cross-translate comments in stack
		try:
			rest = bitrix.bx24.callMethod('task.commentitem.getlist', taskId=id)
			if rest:
				return rest[-1]['AUTHOR_NAME']
		except BitrixError as message:
			return 'ошибка запроса закрывающего пользователя'
	def test_get(): #Cross-translate comments in stack
		try:
			rest = bitrix.bx24.callMethod('tasks.task.list', filter={'REAL_STATUS':'2', 'RESPONSIBLE_ID':'28'}, select=['ID','RESPONSIBLE_ID'])
			if rest:
				return rest
		except BitrixError as message:
			return 'ok'
	def user_task_get(id): #Cross-translate comments in stack
		try:
			rest = bitrix.bx24.callMethod('tasks.task.list', filter={'REAL_STATUS':'2', 'RESPONSIBLE_ID':int(id)})
			if rest:
				return rest
		except BitrixError as message:
			return 'ok'
	
	#def image_upload(id, file): #Cross-translate comments in stack
	def image_upload(id, link): #upload image to bitrix on task end
		#id = 12850
		dir = 187960
		file = link
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		name = file.split("/")
		name = name[-1].split(".")
		name = id + '.' + name[-1]
		resp = urlopen(file, context=ctx)
		try:
			open(name, 'x')
			open(name, 'wb').write(resp.read())
		except FileExistsError:
			os.remove(name)
			open(name, 'x')
			open(name, 'wb').write(resp.read())
		#print(resp.read())
		try:
			rest = bitrix.bx24.callMethod('disk.folder.uploadfile', id=dir)
			if rest:
				url = rest['uploadUrl']
				up = {'file':(name, open(name, 'rb'), "multipart/form-data")}
				request = requests.post(url, files=up)
				result = json.loads(request.text)
				try:
					text = '[DISK FILE ID=n' + str(result["result"]["ID"]) + ']'
					print(id)
					print(text)
					bitrix.comment_add(id, text)
					os.remove(name)
				except KeyError: 
					return 'file error'
		except BitrixError as message:
			return 'ok'
	
	def user_find(str): #Cross-translate comments in stack
		try:
			rest = bitrix.bx24.callMethod('user.get', ID=28)
			if rest:
				return rest
		except BitrixError as message:
			return 'ok'

	def comment_add(id, text): #add comment to task
		try:
			rest = bitrix.bx24.callMethod('task.commentitem.add', taskId=int(id), fields={'POST_MESSAGE': text})
			#task = rest['task']['id']
			print('ccommented')
			return 1
		except BitrixError as message:
			print(message)
			return 0

	def complete(id): #complete task from fresh side
		try:
			rest = bitrix.bx24.callMethod('tasks.task.complete', taskId=id)
			print('completed')
		except BitrixError as message:
			return message

	def delete(id): #obselete but may need in future (deletes task from fresh side)
		try:
			rest = bitrix.bx24.callMethod('tasks.task.delete', taskId=id)
		except BitrixError as message:
			return message
	
	def restart(id): #restarts task by id
		try:
			rest = bitrix.bx24.callMethod('tasks.task.update', taskId=int(id), fields={'STATUS': 2})
		except BitrixError as message:
			return message
		
	def start(id): #restarts task by id
		try:
			rest = bitrix.bx24.callMethod('tasks.task.start', taskId=int(id))
		except BitrixError as message:
			return message
	
	def tag(id, tag_str): #restarts task by id
		try:
			rest = bitrix.bx24.callMethod('tasks.task.update', taskId=int(id), fields={'TAG': tag_str})
		except BitrixError as message:
			return message

	def delegate(id, uid): #delegate task to user with id
		try:
			print(id)
			print(uid)
			#rest = bitrix.bx24.callMethod('tasks.task.delegate', taskId=int(id), userId=int(uid))
			rest = bitrix.bx24.callMethod('tasks.task.delegate', taskId=int(id), userId=int(uid))
		except ValueError:
			return 'азаза'
	
	def attachments(id): #get task attachments and store them in database with all info from task
		url_part = 'https://icstech.bitrix24.ru'
		fp = 'temp/'
		rest = bitrix.bx24.callMethod('tasks.task.get', taskId=id)
		task_title = rest['task']['title']
		task_body = rest['task']['description']
		status = rest['task']['status']
		time_start = rest['task']['createdDate']
		time_start = ciso8601.parse_datetime(time_start)
		time_stop = rest['task']['closedDate']
		time_stop = ciso8601.parse_datetime(time_stop)
		try:
			rest = bitrix.bx24.callMethod('task.commentitem.getlist', taskId=int(id))
			attachments = rest[-2]['ATTACHED_OBJECTS']
			last_comment = rest[-2]['POST_MESSAGE']
			attachmnets_v = attachments.values()
			attachmnets_i = iter(attachmnets_v)
			first_value = next(attachmnets_i)
			url_part2 = first_value['DOWNLOAD_URL']
			fp = fp + first_value['NAME']
			url = url_part + url_part2
			response = requests.get(url)
			img = Image.open(BytesIO(response.content))
			img = img.save(fp)
			image = open(fp, 'rb') 
			image_read = image.read() 
			image_64_encode = base64.encodestring(image_read)
			with connection.cursor() as cursor:
				sql = "INSERT INTO `tasks` (`id`, `title`, `body`, `status`, `stop_comm`, `file`, `timestmp_start`, `timestmp_stop`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (id, task_title, task_body, status, last_comment, image_64_encode, time_start, time_stop))
				connection.commit()
			os.remove(fp)
		except KeyError:
			print("No attachments bruh")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#FRESH OFFICE CLASS BOI
class fresh:
	def creator(fid, conn): #get creator name
		cursor = conn.cursor()
		cursor.execute("""
			SELECT 
				MANAGER_NAME
			FROM 
				MANAGERS
			WHERE ID_MANAGER = %s
		""" % (fid))
		cre = cursor.fetchone()
		return cre 
	def adres(fid, conn): #get adres from another table
		cursor = conn.cursor()
		cursor.execute("""
			SELECT 
				ADRES
			FROM 
				COMPANY
			WHERE ID_COMPANY = %s
		""" % (fid))
		kv_ask = cursor.fetchall()
		adr = str(kv_ask[0])		#adres formating
		adr = adr.replace("'", '')	#adres formating
		adr = adr.replace(',', '')	#adres formating
		adr = adr.replace(')', '')	#adres formating
		adr = adr.replace('(', '')	#adres formating
		return adr 
	def start(comm, fid, conn): #set task status in freshoffice and put commentary in REZULTAT_CONTACT
		cursor = conn.cursor()
		przn = "3"
		query2="update LIST_CONTACT_COMPANY set MARKER_DESCRIPTION='%s', ID_PRIZNAK_CONTACT='%s' where ID_CONTACT = %s" % (comm,przn,fid)
		ret=cursor.execute(query2)
		conn.commit()
		print("db start ok")
	def stop(comm, fid, conn): #set task complete in freshoffice and put commentary in REZULTAT_CONTACT
		cursor = conn.cursor()
		#comm = "Заявка выполнена"
		przn = "2"
		query="update LIST_CONTACT_COMPANY set REZULTAT_CONTACT='%s', ID_PRIZNAK_CONTACT='%s'  where ID_CONTACT = %s" % (comm,przn,fid)
		ret=cursor.execute(query)
		conn.commit()
		print("db stop ok")
	def update(comm, fid, conn): #set task status in freshoffice and put commentary in MARKER_DESCRIPTION
		cursor = conn.cursor()
		przn = "3"
		query2="update LIST_CONTACT_COMPANY set MARKER_DESCRIPTION='%s', ID_PRIZNAK_CONTACT='%s' where ID_CONTACT = %s" % (comm,przn,fid)
		ret=cursor.execute(query2)
		conn.commit()
		print("db update ok")
	def comment(text, fid, conn): #paste comment in "add_prim"
		cursor = conn.cursor()
		query2="update LIST_CONTACT_COMPANY set	 ADD_PRIM_COMPANY='%s'	where ID_CONTACT = %s" % (text,fid)
		ret=cursor.execute(query2)
		conn.commit()
		print("db comment ok")
	def comment_list(date, text, fid, conn): #paste comment in "Примечания исполнителя"
		cursor = conn.cursor()
		space = "  " #just string formatting shit
		comenttime = date.replace("T", " ")
		comenttime = date.replace("Z", "")
		line = "-" #just string formatting shit
		name = "Сотрудник ИКС"
		name2 = comenttime + space + name
		query2="INSERT INTO LIST_PRIM_CONTACTS (ID_CONTACT_COMPANY, DATE_PRIM_COMPANY, MANAGER_NAME_CREATOR, MANAGER_NAME_LAST_CHANCH, PRIM_COMPANY) VALUES (%s, %s, %s, %s, %s)"
		val= (fid, comenttime, name, name2, text)
		ret=cursor.execute(query2, val)
		conn.commit()
		print("db comment_in_list ok")
	def date(text, fid, conn): #paste comment in "Примечания исполнителя"
		completetime = text.replace("T", " ")
		completetime = text.replace("Z", "")
		cursor = conn.cursor()
		query2="update LIST_CONTACT_COMPANY set	 ADD_VYPOLN2='%s'  where ID_CONTACT = %s" % (completetime,fid)
		ret=cursor.execute(query2)
		conn.commit()
		print("db date ok")	
	def status_translate(text): #paste comment in "Примечания исполнителя"
		if text == 2:
			return "Выполнена"
		if text == 4:
			return "Отменена"
	def getall(conn): #main query to get all tasks in freshoffice
		cursor = conn.cursor()
		cursor.execute("""
			SELECT
				*
			FROM 
				ICSTECHBOT_READ_MOUTH
			""")
		t = cursor.fetchall()
		return t
	def getall_2(conn): #main query to get all tasks in freshoffice
		cursor = conn.cursor()
		cursor.execute("""
			SELECT
				*
			FROM 
				ICSTECHBOT_READ_MOUTH
			""")
		t = cursor.fetchall()
		return t
	def num(conn):	#count number of tasks in fresh
		cursor = conn.cursor()
		cursor.execute("""
			SELECT
				COUNT(*)
			FROM 
				ICSTECHBOT_READ_MOUTH
			""")
		t = cursor.fetchone()
		return t
	def progress(count, total, suffix=''):	#just draw progressbar :D
		
		bar_len = 60
		filled_len = int(round(bar_len * count / float(total)))

		percents = round(100.0 * count / float(total), 1)
		bar = '█' * filled_len + ' ' * (bar_len - filled_len)

		sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
		sys.stdout.flush()	# As suggested by Rom Ruben
	def cancel(comm, fid, conn): #set task cancell in freshoffice and put commentary in REZULTAT_CONTACT
		cursor = conn.cursor()
		#comm = "Заявка выполнена"
		name = "Сотрудник ИКС"
		space = "  " #just string formatting shit
		line = "-" #just string formatting shit
		comm = name + space + line + space + comm
		przn = "4"
		query="update LIST_CONTACT_COMPANY set REZULTAT_CONTACT='%s', ID_PRIZNAK_CONTACT='%s'  where ID_CONTACT = %s" % (comm,przn,fid)
		ret=cursor.execute(query)
		conn.commit()
		print("db stop ok")
	def getprim(conn, fid, text): #main query to get all tasks in freshoffice
		cursor = conn.cursor()
		sql = "SELECT COUNT(*) FROM LIST_PRIM_CONTACTS WHERE ID_CONTACT_COMPANY LIKE %s AND PRIM_COMPANY LIKE %s"
		val = (int(fid), str(text))
		cursor.execute(sql, val)
		t = cursor.fetchone()
		return t
	def update_prim(conn, comm, fid): #set task status in freshoffice and put commentary in REZULTAT_CONTACT
		cursor = conn.cursor()
		query2="update LIST_CONTACT_COMPANY set ADD_PRIM='%s' where ID_CONTACT = %s" % (comm,fid)
		ret=cursor.execute(query2)
		conn.commit()
		print("db prim ok")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def free_task_count():
	i = 0
	avrora = 0
	leninskiy = 0
	aviator = 0
	forward = 0
	onetime = 0
	dachniy = 0
	sophia = 0
	head = 0
	progress = 0
	megalit = 0
	moscow = 0
	vika = 0
	katya = 0
	sun = 0
	rainbow = 0
	arr = []
	tid = bitrix.get_group()
	#print(tid['tasks'][i]['id'])
	for row in tid['tasks']:
		task = bitrix.check(tid['tasks'][i]['id'])['task']
		title = task['title']
		uid = task['responsible']['id']
		i = i +1
		print(title)
		#print(title.split('/')[0])
		try:
			if bitrix.name_translate(title.split('/')[0]):
				sysname = bitrix.name_translate(title.split('/')[0])['system_name']
				if sysname == 'avrora':
					avrora += 1
				if sysname == 'leninskiy':
					leninskiy += 1
				if sysname == 'aviator':
					aviator += 1
				if sysname == 'forward':
					forward += 1
				if sysname == 'onetime':
					onetime += 1
				if sysname == 'dachniy':
					dachniy += 1
				if sysname == 'sophia':
					sophia += 1
				if sysname == 'head':
					head += 1
				if sysname == 'progress':
					progress += 1
				if sysname == 'megalit':
					megalit += 1
				if sysname == 'moscow':
					moscow += 1
				if sysname == 'vika':
					vika += 1
				if sysname == 'katya':
					katya += 1
				if sysname == 'sun':
					sun += 1
				if sysname == 'rainbow':
					rainbow += 1
		except TypeError:
			return "ЖК не распознан"
def nn_cleaner(str):
	try:
		print(str.splitlines()[0])
		if '\n' in str:
			print('found carriedge return')
			#str = str.splitlines()
			return str.replace("\n", " ")
		else:
			#str.splitlines()
			return str
	except:
		return str
#fresh_detail = fresh.getall_2(conn)
i = 0
with open('test_det.csv', 'a') as the_file:
	table_header = "дата подачи в цук;	дата завершения;	контрагент;	тело заявки;	id задачи в битрикс;	статус;	ответственный;	закрывший \n"
	the_file.write(re.sub(' +', ' ', table_header))
	for fst_ask in fresh.getall_2(conn): #spaghetty code
		i = i + 1
		print(i)
		cid = fst_ask[1]
		title = fst_ask[10] #task name in freshoffice
		deadline = str(fst_ask[12])
		print(str(fst_ask[4]) + ' / ' + str(fst_ask[12]))
		if not fst_ask[12]:
			deadline = "дата закрытия отсутствует"
		if fst_ask[7] == 2: 
			mainstream = str(fst_ask[4]) + '; ' + str(deadline) + '; ' + fresh.adres(fst_ask[1], conn) + '; ' + str(nn_cleaner(title)) + '; ' + str(fst_ask[30]) + '; ' + str(fresh.status_translate(fst_ask[7])) + '; ' + str(bitrix.comment_get(fst_ask[30])) + '; ' + str(bitrix.check(fst_ask[30]))
		if fst_ask[7] == 4:
			mainstream = str(fst_ask[4]) + '; ' + str(deadline) + '; ' + fresh.adres(fst_ask[1], conn) + '; ' + str(nn_cleaner(title)) + '; ' + str(fst_ask[30]) + '; ' + str(fresh.status_translate(fst_ask[7])) + '; ' + str(bitrix.comment_get(fst_ask[30])) + '; ' + str(bitrix.check(fst_ask[30]))
		the_file.write(re.sub(' +', ' ', mainstream) + '\n')
	print('done')