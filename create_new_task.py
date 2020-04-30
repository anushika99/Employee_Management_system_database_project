""" Employees/Director Adding new Task """
import mail

def checkYear(year): 
    if (year % 4) == 0: 
        if (year % 100) == 0: 
            if (year % 400) == 0: 
                return True
            else: 
                return False
        else: 
             return True
    else: 
        return False


def dateinput(month,year):
	# print("Date Input")
	# print()
	# print("add date : ")
	date=input("Enter date : ")
	if not date.isnumeric():
		print("enter a valid date")
		dateinput(month,year)
	if(int(month) == 1 or int(month) ==3 or int(month) ==5 or int(month) ==7 or int(month) ==8 or int(month) ==10 or int(month) ==12):
		if(int(date)<0 or int(date)>31):
			print("enter valid date!!")
			return(dateinput(month,year))
	if(int(month) ==4 or int(month) ==6 or int(month) ==9 or int(month) ==11):
		if(int(date)<0 or int(date)>30):
			print("enter valid date")
			return(dateinput(month,year))
	if(int(month) ==2):
		if(checkYear(year)):
			if(int(date)<0 or int(date) >29):
				print("enter valid date")
				return(dateinput(month,year))
		if(int(date)<0 or int(date) >28):	
			print("enter valid date")
			return(dateinput(month,year))
	return(date)				
	

def monthinput():
	month=""
	month=input("Enter month : ")
	if not month.isnumeric():
		print("enter a valid month")
		return(monthinput())
	if(int(month)<1 or int(month) >12):
		print("enter a valid month")
		return(monthinput())	
	else:
		return(month)


def yearinput():	
	year=input("Enter Year : ")
	if not year.isnumeric():
		print("enter a valid year")
		return(yearinput())
	if(int(year)<2019 or int(year) >2030):
		print("enter a valid year")
		return(yearinput())	
	return(year)


def date_final():
	
	month=monthinput()
	year=yearinput()
	date=dateinput(month,year)
	due_date=str(year)+"-"+str(month)+"-"+str(date)
	print(due_date)
	print("do you want to finalize this date")
	print("Press y to confirm and any other key to edit")
	ans=str(input())
	if(ans=="y" or ans =="Y"):
		return(due_date)
	return(date_final())	


def emp_Id():
	emp_list = []
	while True:
		emp=input("Enter Employee Id : ")
		if not emp.isnumeric():
			print("enter a valid employee id")
			continue
		emp_list.append(emp)
		op = input('Want to Add Another Employee(Y/N): ')
		if op == 'N':
			break
	return(emp_list)

def task_Id(last_id):
	task=input("enter task id , your last task id was :"+str(last_id)+" : ")
	if not task.isnumeric():
		print("enter a task id")
		return(task_Id())
	return(task)


def create_task(mydb):
	mycursor = mydb.cursor()
	print('------ Creating Tasks --------')
	print()
	count = 1
	mycursor.execute("SELECT * FROM tasks_info")
	result_list =[]
	myresult = mycursor.fetchall()
	count = 1
	for x in myresult:
	    tuple_list = [count, x[0], x[1], x[2], x[3]]
	    count = count + 1
	    result_list.append(tuple_list)
	
	description=str(input("Enter Task Descrpition : "))
	date_due=date_final()
	emp=emp_Id()
	last_id=int(result_list[-1][1])+1
	task=task_Id(last_id)

	sql = "INSERT INTO tasks_info (id,description,Date,status) VALUES (%s,%s,%s,%s)"
	val = (task,description,date_due,'InProgress')
	mycursor.execute(sql,val)
	task_details = 'Description- '+description + ' Deadline- '+ date_due
	for i in emp:
		sql = "INSERT INTO tasks_employee (id,employee_id) VALUES (%s,%s)"
		val = (task, i)
		mycursor.execute(sql, val)
		mail.send_notification_tasks(task_details, mydb, i)
	print('Added the new Task')
	mydb.commit()
	mycursor.close()
	return