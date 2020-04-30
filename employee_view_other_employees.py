
from tabulate import tabulate
import view_info_employee_client


def hr_all_employees(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * from employee_personal_info')
    emp_data = mycursor.fetchall()
    result_list = []
    for x in emp_data:
        tuple_list = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]]
        result_list.append(tuple_list)
    print('Total no. of Employees: ' + str(len(result_list)))
    print(tabulate(result_list,
                   headers=['Employee Id', 'Name', 'Age', 'Gender', 'Address ID', 'Phone', 'Year Of Joining',
                            'Salary', 'Manager ID', 'Designation', 'Department ID', 'Attendance', 'Leaves']))
    mycursor.close()
    return


def hr_employee_dept(mydb):
    mycursor = mydb.cursor()
    # adding check for department name
    while True:
        print("Enter Department Name: ")
        dept_name = input()
        if not view_info_employee_client.check_department(mydb, dept_name):
            print(' Department Name entered wrong, please enter again')
            continue
        break

    mycursor.execute('SELECT dept_id from department WHERE name= "' + str(dept_name) + '"')
    dept_id = mycursor.fetchall()

    dept_id = int(dept_id[0][0])

    mycursor.execute('SELECT * from employee_personal_info WHERE dept_id = ' + str(dept_id))
    emp_data = mycursor.fetchall()
    result_list = []
    for x in emp_data:
        tuple_list = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]]
        result_list.append(tuple_list)
    print('Total no. of Employees: ' + str(len(result_list)))
    print(tabulate(result_list,
                   headers=['Employee Id', 'Name', 'Age', 'Gender', 'Address ID', 'Phone', 'Year Of Joining',
                            'Salary', 'Manager ID', 'Designation', 'Department ID', 'Attendance', 'Leaves']))
    mycursor.close()
    return


def hr_view_specific_employee(mydb):
    mycursor = mydb.cursor()
    # adding check for employee_id
    while True:
        print("Enter Employee ID: ")
        emp_id = input()
        if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
            print('Employee ID entered Wrong, Please Enter again')
            continue
            print()
        break
    mycursor.execute('SELECT * from employee_personal_info WHERE employee_id = ' + str(emp_id))
    emp_data = mycursor.fetchall()
    result_list = []
    for x in emp_data:
        tuple_list = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12]]
        result_list.append(tuple_list)
    print('Total no. of Employees: ' + str(len(result_list)))
    print(tabulate(result_list,
                   headers=['Employee Id', 'Name', 'Age', 'Gender', 'Address ID', 'Phone', 'Year Of Joining',
                            'Salary', 'Manager ID', 'Designation', 'Department ID', 'Attendance', 'Leaves']))
    mycursor.close()
    return


def view_all_employees(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name, phone, manager_id from employee_personal_info');
    emp_data = mycursor.fetchall()
    for i in emp_data:
        mang_id = i[2]
        mycursor.execute('SELECT name, phone from employee_personal_info where employee_id = ' + str(mang_id));
        mang_data = mycursor.fetchall()

        print("Employee Name: " + str(i[0]) + " Employee Contact: " + str(i[1]))
        if (len(mang_data) != 0):
            print("Manager Name: " + str(mang_data[0][0]) + " Manager Contact: " + str(mang_data[0][1]))
        print()
        print()
    mycursor.close()
    return


def view_employee_dept(mydb):
    mycursor = mydb.cursor()
    # adding check for department name
    while True:
        print("Enter Department Name: ")
        dept_name = input()
        if not view_info_employee_client.check_department(mydb, dept_name):
            print(' Department Name entered wrong, please enter again')
            continue
        break
    mycursor.execute('SELECT dept_id from department WHERE name= "' + str(dept_name) + '"');
    dept_id = mycursor.fetchall()

    dept_id = int(dept_id[0][0])

    mycursor.execute(
        'SELECT name, phone, manager_id from employee_personal_info WHERE dept_id = ' + str(dept_id));
    emp_data = mycursor.fetchall()
    for i in emp_data:
        mang_id = i[2]
        mycursor.execute('SELECT name, phone from employee_personal_info where employee_id = ' + str(mang_id));
        mang_data = mycursor.fetchall()

        print("Employee Name: " + str(i[0]) + " Employee Contact: " + str(i[1]))

        if (len(mang_data) != 0):
            print("Manager Name: " + str(mang_data[0][0]) + " Manager Contact: " + str(mang_data[0][1]))
        print()
        print()
    mycursor.close()
    return


def view_specific_employee(mydb):
    mycursor = mydb.cursor()
    # adding check for employee_id
    while True:
        print("Enter Employee ID: ")
        emp_id = input()
        if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
            print('Employee ID entered Wrong, Please Enter again')
            continue
            print()
        break
    mycursor.execute(
        'SELECT name, phone, manager_id from employee_personal_info WHERE employee_id = ' + str(emp_id));
    emp_data = mycursor.fetchall()
    for i in emp_data:
        mang_id = i[2]
        mycursor.execute('SELECT name, phone from employee_personal_info where employee_id = ' + str(mang_id));
        mang_data = mycursor.fetchall()

        print("Employee Name: " + str(i[0]) + " Employee Contact: " + str(i[1]))

        if (len(mang_data) != 0):
            print("Manager Name: " + str(mang_data[0][0]) + " Manager Contact: " + str(mang_data[0][1]))
        print()
        print()
    mycursor.close()
    return