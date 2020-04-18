############# client tasks Information ###############3

# Import Statement
from tabulate import tabulate


# see the information of employees working on a task
def task_employee_info(mydb, task_id):
    mycursor = mydb.cursor()
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
    mycursor.close()
    return


# prints the current project list
def client_project_info_current(mydb,id):
    mycursor = mydb.cursor()
    print('----------Current Projects------')
    print()
    query = 'SELECT id, description, date, status FROM tasks_info WHERE (status =\'InProgress\' OR  status = \'Ongoing\') AND id IN(SELECT task_id FROM clients_project WHERE id=' + str(id) +')'
    mycursor.execute(query)
    result_list = []
    myresult = mycursor.fetchall()
    count = 1
    task_id_list = []
    for x in myresult:
        task_id_list.append(x[0])
        tuple_list = [count, x[1], x[2],x[3]]
        count = count +1
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Project Description', 'Deadline', 'Status']))
    print()
    print('Total number of current projects: '+str(len(result_list)))

    # option of seeing the employees working on a project
    ch = input('Want to see Contact Information of Employees Working on the Project(Y/N): ')
    while ch == 'Y':
        op = int(input('Enter the project Serial Number: '))
        task_id = task_id_list[op - 1]
        task_employee_info(mydb,task_id)
        op = input('Continue/Back: ')
        if op == 'Back':
            ch == 'N'
            break
    mycursor.close()
    return


# # view details of past project of client
# def client_project_info_past(mycursor,id):
