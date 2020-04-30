import smtplib, requests, time

def send_notification_meetings(text,mydb, id):
	mycursor = mydb.cursor()
	gmail_user = 'dbmsproject84'
	gmail_password = 'Dbms@123'
	sent_from = gmail_user
	mycursor.execute('SELECT email FROM email_id WHERE id = '+ str(id))
	myresult = mycursor.fetchall()
	# print(myresult)

	# to = "dbmsproject84@gmail.com"
	to = myresult[0][0]
	subject = 'New meeting scheduled'
	email_text = text
	# print(email_text)
	#email send request
	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sent_from, to, email_text)
	    server.close()

	    print ('Email sent!')
	except Exception as e:
	    print(e)
	    print ('Something went wrong...')
	mycursor.close()


def send_notification_tasks(text, mydb, id):
	mycursor = mydb.cursor()
	gmail_user = 'dbmsproject84'
	gmail_password = 'Dbms@123'
	sent_from = gmail_user
	mycursor.execute('SELECT email FROM email_id WHERE id = ' + str(id))
	myresult = mycursor.fetchall()
	# to = "dbmsproject84@gmail.com"
	to = myresult[0][0]
	Subject = "Please find the new task alloted"
	email_text = text
	#email send request
	try:
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sent_from, to, email_text)
	    server.close()

	    print ('Email sent!')
	except Exception as e:
	    print(e)
	    print ('Something went wrong...')
	mycursor.close()
# import mysql.connector
# # send_notification_tasks('hello')
# mydb = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='anushi123',
#     database='dbms'
#   )
# send_notification_meetings('Purpose- Report discussion Date & Time- 2021-3-1 08:30:00  Caller- Xavier Attendees- Marcus-lee,', mydb, 0)
