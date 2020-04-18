###### Main head Uses this to view the details of all the tasks in the company #####

# Import Statement
import mysql.connector
from tabulate import tabulate


# see the information of employees working on a task
def task_employee_info(mycursor, task_id):
    query = 'SELECT employee_personal_info.name, phone, designation, department.name FROM  employee_personal_info, department WHERE employee_personal_info.dept_id = department.dept_id AND employee_id IN(SELECT employee_id FROM tasks_employee WHERE id =' + str(task_id)+')'
    mycursor.execute(query)
    result_list = []
    myresult = mycursor.fetchall()
    count = 1
    for x in myresult:
        tuple_list = [count, x[0], x[1], x[2], x[3]]
        count = count + 1
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Name', 'Contact No. ', 'Designation', 'Department']))
    return


# view all the tasks
def view_tasks(mydb):
	mycursor = mydb.cursor()
	print('------Tasks --------')
	print()
	mycursor.execute("SELECT * FROM tasks_info")
	result_list =[]
	myresult = mycursor.fetchall()
	count = 1
	for x in myresult:
	    tuple_list = [count, x[0], x[1], x[2], x[3]]
	    count = count + 1
	    result_list.append(tuple_list)
	print(tabulate(result_list, headers=['S.No', 'Task Id', 'Task description', 'Due Date', 'Status']))
	print()

	# option of seeing the employees working on a project
	ch = input('Want to see Contact Information of Employees Working on the Project(Y/N): ')
	while ch == 'Y':
		task_id = int(input('Enter the Task Id: '))
		task_employee_info(mycursor, task_id)
		op = input('Continue/Back: ')
		if op == 'Back':
			ch == 'N'
			break
	mycursor.close()
	return