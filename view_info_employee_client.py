""" director views info of a employee/client """
from tabulate import tabulate


# view all the employees of the company
def view_all_employee(mydb):
    mycursor = mydb.cursor()
    print('------ Employees -----')
    print()
    mycursor.execute('SELECT employee_id, name FROM employee_personal_info')
    myresult = mycursor.fetchall()
    result_list = []
    for x in myresult:
        tuple_list = [x[0], x[1]]
        result_list.append(tuple_list)
    print('Total no. of Employees: '+ str(len(result_list)))
    print(tabulate(result_list, headers=['Employee Id', 'Name']))
    print()
    mycursor.close()
    return


# check whether department entered is correct or not
def check_department(mydb, dept):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name FROM department')
    departments = []
    myresult = mycursor.fetchall()
    mycursor.close()
    for x in myresult:
        departments.append(x[0])
    if dept in departments:
        return True
    return False


# view all the employees of department
def view_employee_department(mydb, dept):
    mycursor = mydb.cursor()
    print('--------Department ' + dept + '----------')
    print()
    query = 'SELECT employee_id, name FROM employee_personal_info WHERE dept_id IN (SELECT dept_id FROM department WHERE name = \''+ dept+'\')'
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    result_list = []
    for x in myresult:
        tuple_list = [x[0], x[1]]
        result_list.append(tuple_list)
    print('Total no. of Employees in the department: ' + str(len(result_list)))
    print(tabulate(result_list, headers=['Employee Id', 'Name']))
    print()
    mycursor.close()
    return


# check whether employee id is correct or not
def check_emp_id(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT employee_id FROM employee_personal_info')
    emp_ids = []
    myresult = mycursor.fetchall()
    mycursor.close()
    for x in myresult:
        emp_ids.append(x[0])
    if id in emp_ids:
        return True
    return False


# viewing a specific employee Info employee Info
def view_employee_info(mydb,emp_id):
    mycursor = mydb.cursor()
    print('--Personal Info--')
    mycursor.execute('SELECT * FROM employee_personal_info WHERE employee_id = '+str(emp_id))
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Employee_id :',x[0])
        print('Name: ', x[1])
        print('Age: ',x[2])
        print('Gender: ', x[3])
        # finding the address using the address id
        mycursor.execute('SELECT addr FROM address WHERE id = '+str(x[4]))
        add_result = mycursor.fetchall()
        for y in add_result:
            print('Address: ', y[0])
        print('Contact no: ', x[5])
        print('Year of Joining: ', x[6])
        print('Salary; ',x[7])
        # finding the name of manager
        mycursor.execute('SELECT name FROM employee_personal_info WHERE employee_id = '+str(x[8]))
        manager_result = mycursor.fetchall()
        for y in manager_result:
            print('Manager: ', y[0])
        print('Designation: ', x[9])
        # finding the department name
        mycursor.execute('SELECT name FROM department WHERE dept_id = ' + str(x[10]))
        department_result = mycursor.fetchall()
        for y in department_result:
            print('Department: ', y[0])
        print('No. of leaves: ',x[11])
        print('Attendance: ', x[12])
    print()
    print('-- Performance--')
    mycursor.execute('SELECT * FROM Employee_Performance WHERE id = '+ str(emp_id))
    myresult = mycursor.fetchall()
    for x in myresult:
        print('No. of Tasks Completed: ', x[1])
        print('Backlogs: ', x[2])
        print('Communication Skills(Scale 1-10): ', x[3])
        print('Output Quality(Scale 1-10): ', x[4])
        print('Analytic Skills(Scale 1-10): ', x[5])

    mycursor.close()
    return


# view all the clients
def view_all_clients(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id, company_name FROM clients')
    myresult = mycursor.fetchall()
    mycursor.close()
    result_list = []
    for x in myresult:
        tuple_list = [x[0], x[1]]
        result_list.append(tuple_list)
    print('Total no. of Clients' + str(len(result_list)))
    print(tabulate(result_list, headers=['Client Id', 'Client Name']))
    print()
    return


# check client id is correct or not
def check_client_id(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM clients')
    clients_ids = []
    myresult = mycursor.fetchall()
    mycursor.close()
    for x in myresult:
        clients_ids.append(x[0])
    if id in clients_ids:
        return True
    return False


# view all the information of a specific client
def view_client(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT clients.id, clients.company_name, address.addr, clients.phone FROM clients, address WHERE clients.company_address_id = address.id AND clients.id = '+str(id))
    myresult = mycursor.fetchall()
    mycursor.close()
    print()
    for x in myresult:
        print('Client Id: ', x[0])
        print('Company Name: ', x[1])
        print('Address: ', x[2])
        print('Contact No. :', x[3])
    print()
    return

