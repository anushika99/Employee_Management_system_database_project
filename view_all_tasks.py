""" Main head Uses this to view the details of all the tasks in the company or employee to see the tasks he is working on"""

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
    if len(result_list) == 0:
        print('No employee working in the task')
        return
    print(tabulate(result_list, headers=['S.No', 'Name', 'Contact No. ', 'Designation', 'Department']))
    mycursor.close()
    return


# other employees working on a task
def task_other_employee_info(mycursor, task_id, id):
    query = 'SELECT employee_personal_info.name, phone, designation, department.name FROM  employee_personal_info, department WHERE employee_personal_info.dept_id = department.dept_id AND employee_id IN(SELECT employee_id FROM tasks_employee WHERE id =' + str(task_id)+') AND employee_id != ' + str(id)
    mycursor.execute(query)
    result_list = []
    myresult = mycursor.fetchall()
    count = 1
    for x in myresult:
        tuple_list = [count, x[0], x[1], x[2], x[3]]
        count = count + 1
        result_list.append(tuple_list)
    if len(result_list) == 0:
        print('No other employeees working on the task')
        print()
        return
    print(tabulate(result_list, headers=['S.No', 'Name', 'Contact No. ', 'Designation', 'Department']))
    return


# view tasks of specific employee
def view_tasks_employee(mydb, id):
    mycursor = mydb.cursor()
    print('------Tasks --------')
    print()
    mycursor.execute("SELECT * FROM tasks_info WHERE (status = \"InProgress\" OR status = \"Ongoing\") AND id in (SELECT id FROM tasks_employee WHERE employee_id = " + str(id)+")")
    result_list = []
    myresult = mycursor.fetchall()
    count = 1
    for x in myresult:
        tuple_list = [count, x[0], x[1], x[2], x[3]]
        count = count + 1
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Task Id', 'Task description', 'Due Date', 'Status']))
    print()

    # option of seeing the other employees working on a project
    ch = input('Want to see Contact Information of other Employees Working on the Task(Y/N): ')
    while ch == 'Y':
        task_id = int(input('Enter the Task Id: '))
        task_other_employee_info(mycursor, task_id, id)
        op = input('Continue/Back: ')
        if op == 'Back':
            ch == 'N'
            break
    mycursor.close()
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
