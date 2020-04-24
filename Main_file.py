# Import Statements
import mysql.connector
from tabulate import tabulate
import string
import random
from datetime import datetime

# importing python files
import View_Job_openings
import View_Workshops
import Check_login_id
import Client_project_info
import view_all_tasks
import view_info_employee_client
import sys
import create_new_task
import Meetings
import Company_stats
import Update_password_personalInfo

# connecting to mysql database
# run command pip install mysql-connector-python to use the default caching_sha2_password plugin
def connect_database():
  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='anushi123',
    database='dbms'
  )
  return mydb


# employee function
def employee(mydb, id):
    mycursor = mydb.cursor()
    # Finding Employee Name
    mycursor.execute('SELECT name FROM employee_personal_info WHERE employee_id= ' + str(id))
    myresult = mycursor.fetchall()
    emp_name = '--------Welcome '
    for x in myresult:
        emp_name = emp_name + x[0] + '--------------'
    # print(emp_name)
    # print()
    mycursor.execute('SELECT dept_id FROM employee_personal_info WHERE manager_id=' + str(id))
    myresult = mycursor.fetchall()
    len_subs = len(myresult)

    mycursor.execute('SELECT dept_id FROM employee_personal_info WHERE employee_id=' + str(id))
    myresult = mycursor.fetchall()

    # print(myresult[0][0])

    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # check for HR employee -- checking whether department_id is 1 or not
    if int(myresult[0][0]) == 1:
        print('1. View Information')
        print('2. View Tasks')
        print('3. Create new Task ')
        print('4. View Meetings')
        print('5. Schedule new meeting')
        print('6. Update Password')
        print('7. Update Personal Info')
        print('8. View Leave Request')
        print('9. Apply for Leave')
        print('10. View leave Status')
        print('11. View all the employees')
        print('12. View all Employees of a specific Department')
        print('13. View Information of a specific Employee')
        print('14. Edit tasks')
        print('15. Edit Meeting')
        print('16. Edit Employee Performance')
        print('17. Add/Remove an Employee')
        print('18. Add/Remove a Client')
        print('0. Logout')

        choice = int(input())

        if choice == 0:
            login_menu(mydb)
        elif choice == 1:
            view_info_employee_client.view_employee_info(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 2:
            view_all_tasks.view_tasks_employee(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 3:
            create_new_task.create_task(mydb)
            print()
            employee(mydb, id)
        elif choice == 4:
            Meetings.view_meetings(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 5:
            Meetings.call_new_meeting(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 6:
            Update_password_personalInfo.update_password(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 7:
            Update_password_personalInfo.update_personal_info(mydb, id)
            print()
            employee(mydb, id)
        # updating the leave requests
        if choice == 8:
            mycursor.execute(
                'SELECT T1.*,T2.name  FROM leave_request as T1, employee_personal_info as T2 WHERE T1.manager_id=' + str(
                    id) + ' and T1.employee_id = T2.employee_id')
            lis_request = mycursor.fetchall()
            if len(lis_request) == 0:
                print("NO LEAVE REQUEST")
            else:
                for i in lis_request:
                    print("Name: " + str(i[6]) + " Employee Id: " + str(i[0]) + " From: " + str(i[2]) + " To: " + str(
                        i[3]) + " Reason: " + str(i[4]))
                print("Update Leave Status? Y/N")
                choice = input()

                if choice == "Y" or choice == "y":
                    print("Enter Employee id: ")
                    emp_id = int(input())
                    print("Approve? Y/N")
                    choice = input()
                    if choice == "Y" or choice == "y":
                        mycursor.execute('UPDATE leave_request SET status = 1 WHERE employee_id = ' + str(emp_id))
                        mydb.commit()
                    else:
                        mycursor.execute('UPDATE leave_request SET status = -1 WHERE employee_id = ' + str(emp_id))
                        mydb.commit()

                else:
                    pass
            employee(mydb, id)
        # Applying for leaves
        elif choice == 9:
            mycursor.execute('SELECT manager_id from employee_personal_info where employee_id = ' + str(id))
            mang_id = mycursor.fetchall()
            # Verification of Date can be done here
            print("From (YYYY--MM--DD): ")
            start_date = input()
            print("To (YYYY--MM--DD): ")
            end_date = input()
            print("Reason for leave: ")
            Reason = input()
            insert_query = 'insert into leave_request values(' + str(id) + ', ' + str(
                (mang_id[0][0])) + ',  "' + start_date + '", "' + end_date + '", "' + Reason + '", 0 )'
            print(insert_query)
            mycursor.execute(insert_query);
            print("Your request has been submitted")
            mydb.commit()
            print()
            employee(mydb, id)
        # view leave status
        elif choice == 10:
            mycursor.execute('SELECT status from leave_request where employee_id = ' + str(id))
            status_val = mycursor.fetchall()
            status_val = status_val[0][0]
            if (status_val == 0):
                print("Leaves Request is pending")
            if (status_val == 1):
                print("Leaves Request is ACCEPTED")
            if (status_val == -1):
                print("Leaves Request is NOT ACCEPTED")
            employee(mydb, id)

        # viewing all the employees
        elif choice == 11:
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
            print()
            employee(mydb, id)

        # Viewing all the employees of a specific department
        elif choice == 12:
            print()
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
            print()
            employee(mydb, id)

        # View information of a specifc employee
        elif choice == 13:
            print()
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
            print()
            employee(mydb, id)

        # Edit task
        elif choice == 14:
            print()
            print("a. Edit task Description")
            print("b. Add an employee to task")
            print("c. Remove an employee from task")
            inp = input()

            if inp == 'a':
                done = False
                while done == False:
                    print()
                    print('Enter Task ID: ')
                    task_id = input()
                    try:
                        mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
                        # temp = mycursor.fetchall()

                        done = True

                    except:
                        print("Invalid Task ID, Please Enter Again")
                if done:
                    curr_descrip = mycursor.fetchall()
                    curr_descrip = curr_descrip[0][0]
                    print("Current Description: " + str(curr_descrip))
                    print()
                    print("Enter new Description: ")
                    new_description = input()
                    mycursor.execute(
                        'UPDATE tasks_info SET description = "' + str(new_description) + '" WHERE id = ' + str(
                            task_id))  # check new_description
                    mydb.commit()
                    print("Update Made")

            if inp == 'b':
                done = False
                while (done == False):
                    print()
                    print('Enter Task ID: ')
                    task_id = input()
                    try:
                        mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
                        temp = mycursor.fetchall()
                        done = True

                    except:
                        print("Invalid Task ID")

                if (done):
                    # check for employee ID added
                    while True:
                        print("Enter New Employee ID: ")
                        new_emp = input()
                        if not view_info_employee_client.check_emp_id(mydb, int(new_emp)):
                            print('Employee ID entered Wrong, Please Enter again')
                            continue
                            print()
                        break
                    mycursor.execute(' insert into tasks_employee values( ' + str(task_id) + ', ' + str(new_emp) + ')');
                    mydb.commit()
                    print("Update Made")

            if inp == 'c':
                # check for employee ID added
                while True:
                    print("Enter Employee ID: ")
                    emp = input()
                    if not view_info_employee_client.check_emp_id(mydb, int(emp)):
                        print('Employee ID entered Wrong, Please Enter again')
                        print()
                        continue
                    break
                # print("Enter Employee ID: ")
                # emp = input()
                print("Enter Task ID: ")
                task_id = input()
                mycursor.execute(
                    ' DELETE FROM tasks_employee WHERE employee_id = ' + str(emp) + ' and id = ' + str(task_id))
                mydb.commit()
                print("Update Made")
                employee(mydb, id)
            employee(mydb, id)

        elif choice == 15:

            print()
            # added the condition that show meeting after current date time
            mycursor.execute('SELECT count(*) from Meetings WHERE caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
            count_meetings = mycursor.fetchall()
            if len(count_meetings) == 0:
                print("You have not scheduled any meetings")
                employee(mydb, id)
            else:
                print("a. Edit Meeting Information")
                print("b. Add New Employee")
                print("c. Remove Employee")
                inp = input()

                if inp == 'a':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:

                        print("Current Description: " + meeting_details[0][1])
                        print("Current Date and Time: " + str(meeting_details[0][2]))
                        print()
                        print("Enter New Description (-1 for no Change): ")
                        new_description = input()
                        if (new_description == '-1'):
                            new_description = meeting_details[0][1]
                        print("Enter New Date-Time(YYYY--MM--DD HH:MM:SS) (-1 for no Change): ")
                        new_time = input()
                        if new_time == '-1':
                            new_time = meeting_details[0][2]
                        mycursor.execute(
                            'UPDATE Meetings SET purpose = "' + str(new_description) + '" WHERE id = ' + str(
                                meeting_id))
                        mydb.commit()
                        mycursor.execute(
                            'UPDATE Meetings SET date = "' + str(new_time) + '" WHERE id = ' + str(meeting_id))
                        mydb.commit()
                # added check for employee_id
                if inp == 'b':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    # added check for date in meeting
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:
                        while True:
                            print('Enter Employee ID: ')
                            emp_id = input()
                            if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                                print('Wrong Employee ID entered, enter again')
                                continue
                            break
                        mycursor.execute('SELECT * from Meetings_employee WHERE id = ' + str(
                            meeting_id) + ' and employee_id= ' + str(emp_id));

                        meeting_details = mycursor.fetchall()
                        if (len(meeting_details) == 0):
                            mycursor.execute(
                                'insert into Meetings_employee values( ' + str(meeting_id) + ', ' + str(emp_id) + ')')
                        else:
                            print("Employee Already in list")

                if (inp == 'c'):
                    print()
                    print("Enter Meeting ID: ")
                    meeting_id = input()
                    while True:
                        print('Enter Employee ID: ')
                        emp_id = input()
                        if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                            print('Wrong Employee ID entered, enter again')
                            continue
                        break
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'');
                    meeting_details = mycursor.fetchall()
                    if (len(meeting_details) == 0):
                        print("Wrong Meeting ID")
                    else:
                        mycursor.execute(
                            'DELETE from Meetings_employee WHERE id = ' + str(meeting_id) + ' and employee_id= ' + str(
                                emp_id))
                        mydb.commit()

            employee(mydb, id)

        elif (choice == 16):

            print()
            print("Enter Employee ID: ")
            emp_id = input()
            mycursor.execute(
                'SELECT * from employee_personal_info WHERE employee_id = ' + str(emp_id) + ' and manager_id = ' + str(
                    id))
            data = mycursor.fetchall()

            if (len(data) == 0):
                print("Invalid Employee ID")

            else:
                mycursor.execute('SELECT * from Employee_Performance WHERE id = ' + str(emp_id));
                performance_data = mycursor.fetchall()

                print("Tasks Completed: " + str(performance_data[0][1]))
                print("Backlogs: " + str(performance_data[0][2]))
                print("Communication Skills: " + str(performance_data[0][3]))
                print("Output Quality: " + str(performance_data[0][4]))
                print("Analytic Skills: " + str(performance_data[0][5]))

                print()
                print("Update Tasks Completed (-1 for no change): ")
                new_task = input()
                if (new_task == '-1'):
                    new_task = str(performance_data[0][1])

                print("Update Backlogs (-1 for no change): ")
                new_backs = input()
                if (new_backs == '-1'):
                    new_backs = str(performance_data[0][2])

                print("Update Communication Skills (-1 for no change): ")
                new_comm = input()
                if (new_comm == '-1'):
                    new_comm = str(performance_data[0][3])

                print("Update Output Quality (-1 for no change): ")
                new_qual = input()
                if (new_qual == '-1'):
                    new_qual = str(performance_data[0][4])

                print("Update Analytic Skills (-1 for no change): ")
                new_skill = input()
                if (new_skill == '-1'):
                    new_skill = str(performance_data[0][5])

                mycursor.execute(
                    'UPDATE Employee_Performance SET task_complete = ' + str(new_task) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET backlogs = ' + str(new_backs) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET comm_skill = ' + str(new_comm) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET output_quality = ' + str(new_qual) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET analytic_skill = ' + str(new_skill) + ' WHERE id = ' + str(
                        emp_id))
                mydb.commit()

            employee(mydb, id)

        elif (choice == 17):
            print()
            print("Enter Choice (Add/Remove): ")
            val = input()
            val = (val.lower())

            if (val == 'add'):
                mycursor.execute('SELECT count(*) FROM employee_personal_info');
                last_id = mycursor.fetchall()
                last_id = int(last_id[0][0])

                print("Create New Address? (Y/N)")
                addr_stat = input()
                last_addr_id = 0
                if ((addr_stat.lower()) == 'y'):
                    print("Enter City: ")
                    city = input()
                    print("Enter State: ")
                    state = input()
                    print("Enter Pincode: ")
                    pin = input()
                    print("Enter Address: ")
                    addr = input()

                    mycursor.execute('SELECT count(*) FROM address');
                    last_addr_id = mycursor.fetchall()
                    last_addr_id = int(last_addr_id[0][0])

                    mycursor.execute(
                        'insert into address values(' + str(last_addr_id) + ', "' + str(city) + '", "' + str(
                            state) + '", "' + str(pin) + '", "' + str(addr) + '")')
                    mydb.commit()

                else:
                    print()
                    print("Enter Address ID: ")
                    last_addr_id = input()

                print()
                print("Enter Employee Name: ")
                name = input()
                print("Enter Employee Age: ")
                age = input()
                print("Enter Employee Gender: ")
                gender = input()

                print("Enter Employee Phone: ")
                phone = input()

                print("Enter Employee Year of Joining: ")
                yoj = input()

                print("Enter Employee Salary: ")
                salary = input()

                print("Enter Employee's Manager ID: ")
                mang_id = input()

                print("Enter Employee Designation: ")
                desig = input()

                print("Enter Employee Department ID: ")
                dept = input()

                mycursor.execute(
                    'insert into employee_personal_info values( ' + str(last_id) + ', "' + str(name) + '", ' + str(
                        age) + ', "' + str(gender) + '", ' + str(last_addr_id) + ', ' + str(phone) + ', ' + str(
                        yoj) + ', ' + str(salary) + ', ' + str(mang_id) + ', "' + str(desig) + '", ' + str(
                        dept) + ', 0, 0)');
                mydb.commit()
                letters = string.ascii_lowercase
                passkey = ''.join(random.choice(letters) for i in range(10))
                mycursor.execute('insert into Employee_UserId values( ' + str(last_id) + ', "' + str(passkey) + '")')
                mydb.commit()
            else:
                print()
                print("Enter Employee ID: ")
                emp_id = input()
                mycursor.execute('SELECT manager_id FROM employee_personal_info WHERE employee_id = '+emp_id)
                myresult = mycursor.fetchall()
                manager_id = myresult[0][0]
                mycursor.execute('SELECT employee_id FROM employee_personal_info WHERE manager_id = '+ emp_id)
                myresult = mycursor.fetchall()
                for x in myresult:
                    mycursor.execute('UPDATE employee_personal_info SET manager_id = '+str(manager_id)+' WHERE employee_id =  '+str(x[0]))
                    mydb.commit()
                mycursor.execute('SELECT intern_id FROM Intern WHERE manager_id = '+emp_id)
                myresult = mycursor.fetchall()
                for x in myresult:
                    mycursor.execute('UPDATE Intern SET manager_id = '+str(manager_id)+' WHERE intern_id = '+str(x[0]))
                    mydb.commit()
                mycursor.execute('DELETE FROM Employee_Performance WHERE id = '+ emp_id)
                mycursor.execute('DELETE FROM Employee_UserID WHERE id = ' + emp_id)
                mycursor.execute('DELETE FROM tasks_employee WHERE employee_id = ' + emp_id)
                mycursor.execute('DELETE FROM Meetings_employee WHERE employee_id = ' + emp_id)
                mycursor.execute('DELETE FROM Meetings WHERE caller_id = ' + emp_id)
                mycursor.execute('DELETE FROM employee_personal_info WHERE employee_id = ' + str(emp_id))
                mydb.commit()
            employee(mydb, id)

        elif choice == 18:
            print()
            print("Enter Choice (Add/Remove): ")
            val = input()
            val = (val.lower())

            if (val == 'add'):
                mycursor.execute('SELECT count(*) FROM clients');
                last_id = mycursor.fetchall()
                last_id = int(last_id[0][0])

                print("Create New Address? (Y/N)")
                addr_stat = input()
                last_addr_id = 0;
                if ((addr_stat.lower()) == 'y'):
                    print("Enter City: ")
                    city = input()
                    print("Enter State: ")
                    state = input()
                    print("Enter Pincode: ")
                    pin = input()
                    print("Enter Address: ")
                    addr = input()

                    mycursor.execute('SELECT count(*) FROM address');
                    last_addr_id = mycursor.fetchall()
                    last_addr_id = int(last_addr_id[0][0])

                    mycursor.execute(
                        'insert into address values(' + str(last_addr_id) + ', "' + str(city) + '", "' + str(
                            state) + '", "' + str(pin) + '", "' + str(addr) + '")');
                    mydb.commit()

                else:
                    print()
                    print("Enter Address ID: ")
                    last_addr_id = input();

                print()
                print("Enter Client Name: ")
                name = input()
                print("Enter Client Phone: ")
                phone = input()

                mycursor.execute('insert into clients values( ' + str(last_id) + ', "' + str(name) + '", ' + str(
                    last_addr_id) + ', ' + str(phone) + ')');
                mydb.commit()

                letters = string.ascii_lowercase
                passkey = ''.join(random.choice(letters) for i in range(10))
                mycursor.execute('insert into Client_UserId values( ' + str(last_id) + ', "' + str(passkey) + '")')
                mydb.commit()

            else:
                print()
                print("Enter Client ID: ")
                client_id = input()
                mycursor.execute('DELETE FROM clients_project WHERE id = '+client_id)
                mycursor.execute('DELETE FROM Client_UserId WHERE id = ' + str(client_id))
                mydb.commit()
                mycursor.execute('DELETE FROM clients WHERE id = ' + str(client_id))
                mydb.commit()
            employee(mydb, id)


    # user is a manager
    elif (len_subs > 0):
        print('1. View Information')
        print('2. View Tasks')
        print('3. Create new Task ')
        print('4. View Meetings')
        print('5. Schedule new meeting')
        print('6. Update Password')
        print('7. Update Personal Info')
        print('8. View Leave Request')
        print('9. Apply for Leave')
        print('10. View leave Status')
        print('11. View all the employees')
        print('12. View all Employees of a specific Department')
        print('13. View Information of a specific Employee')
        print('14. Edit tasks')
        print('15. Edit Meeting')
        print('16. Edit Employee Performance')
        print('0. Logout')

        choice  = int(input('Enter Choice'))
        if choice == 0:
            login_menu(mydb)
        elif choice == 1:
            view_info_employee_client.view_employee_info(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 2:
            view_all_tasks.view_tasks_employee(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 3:
            create_new_task.create_task(mydb)
            print()
            employee(mydb, id)
        elif choice == 4:
            Meetings.view_meetings(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 5:
            Meetings.call_new_meeting(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 6:
            Update_password_personalInfo.update_password(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 7:
            Update_password_personalInfo.update_personal_info(mydb, id)
            print()
            employee(mydb, id)
        # updating the leave requests
        if choice == 8:
            mycursor.execute(
                'SELECT T1.*,T2.name  FROM leave_request as T1, employee_personal_info as T2 WHERE T1.manager_id=' + str(
                    id) + ' and T1.employee_id = T2.employee_id')
            lis_request = mycursor.fetchall()
            if len(lis_request) == 0:
                print("NO LEAVE REQUEST")
            else:
                for i in lis_request:
                    print("Name: " + str(i[6]) + " Employee Id: " + str(i[0]) + " From: " + str(i[2]) + " To: " + str(
                        i[3]) + " Reason: " + str(i[4]))
                print("Update Leave Status? Y/N")
                choice = input()

                if choice == "Y" or choice == "y":
                    print("Enter Employee id: ")
                    emp_id = int(input())
                    print("Approve? Y/N")
                    choice = input()
                    if choice == "Y" or choice == "y":
                        mycursor.execute('UPDATE leave_request SET status = 1 WHERE employee_id = ' + str(emp_id))
                        mydb.commit()
                    else:
                        mycursor.execute('UPDATE leave_request SET status = -1 WHERE employee_id = ' + str(emp_id))
                        mydb.commit()

                else:
                    pass
            employee(mydb, id)

        # Applying for leaves
        elif choice == 9:
            mycursor.execute('SELECT manager_id from employee_personal_info where employee_id = ' + str(id))
            mang_id = mycursor.fetchall()
            # Verification of Date can be done here
            print("From (YYYY--MM--DD): ")
            start_date = input()
            print("To (YYYY--MM--DD): ")
            end_date = input()
            print("Reason for leave: ")
            Reason = input()
            insert_query = 'insert into leave_request values(' + str(id) + ', ' + str(
                (mang_id[0][0])) + ',  "' + start_date + '", "' + end_date + '", "' + Reason + '", 0 )'   ######## DOUBT HERE(Check reason) ####
            print(insert_query)
            mycursor.execute(insert_query);
            print("Your request has been submitted")
            mydb.commit()
            print()
            employee(mydb, id)
        # view leave status
        elif choice == 10:
            mycursor.execute('SELECT status from leave_request where employee_id = ' + str(id))
            status_val = mycursor.fetchall()
            status_val = status_val[0][0]
            if (status_val == 0):
                print("Leaves Request is pending")
            if (status_val == 1):
                print("Leaves Request is ACCEPTED")
            if (status_val == -1):
                print("Leaves Request is NOT ACCEPTED")
            employee(mydb, id)

        elif (choice == 11):
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
            employee(mydb, id)


        elif (choice == 12):
            print()
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
            employee(mydb, id)


        elif choice == 13:
            print()
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
            employee(mydb, id)

        # Edit task
        elif choice == 14:
            print()
            print("a. Edit task Description")
            print("b. Add an employee to task")
            print("c. Remove an employee from task")
            inp = input()

            if inp == 'a':
                done = False
                while done == False:
                    print()
                    print('Enter Task ID: ')
                    task_id = input()
                    try:
                        mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
                        # temp = mycursor.fetchall()

                        done = True

                    except:
                        print("Invalid Task ID, Please Enter Again")
                if done:
                    curr_descrip = mycursor.fetchall()
                    curr_descrip = curr_descrip[0][0]
                    print("Current Description: " + str(curr_descrip))
                    print()
                    print("Enter new Description: ")
                    new_description = input()
                    mycursor.execute(
                        'UPDATE tasks_info SET description = "' + str(new_description) + '" WHERE id = ' + str(
                            task_id))  # check new_description
                    mydb.commit()
                    print("Update Made")

            if inp == 'b':
                done = False
                while (done == False):
                    print()
                    print('Enter Task ID: ')
                    task_id = input()
                    try:
                        mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
                        temp = mycursor.fetchall()
                        done = True

                    except:
                        print("Invalid Task ID")

                if (done):
                    # check for employee ID added
                    while True:
                        print("Enter New Employee ID: ")
                        new_emp = input()
                        if not view_info_employee_client.check_emp_id(mydb, int(new_emp)):
                            print('Employee ID entered Wrong, Please Enter again')
                            continue
                            print()
                        break
                    mycursor.execute(' insert into tasks_employee values( ' + str(task_id) + ', ' + str(new_emp) + ')');
                    mydb.commit()
                    print("Update Made")

            if inp == 'c':
                # check for employee ID added
                while True:
                    print("Enter Employee ID: ")
                    emp = input()
                    if not view_info_employee_client.check_emp_id(mydb, int(emp)):
                        print('Employee ID entered Wrong, Please Enter again')
                        continue
                        print()
                    break
                # print("Enter Employee ID: ")
                # emp = input()
                print("Enter Task ID: ")
                task_id = input()
                mycursor.execute(
                    ' DELETE FROM tasks_employee WHERE employee_id = ' + str(emp) + ' and id = ' + str(task_id))
                mydb.commit()
                print("Update Made")
                employee(mydb, id)
            employee(mydb, id)

        elif choice == 15:

            print()
            # added the condition that show meeting after current date time
            mycursor.execute('SELECT count(*) from Meetings WHERE caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
            count_meetings = mycursor.fetchall()
            if len(count_meetings) == 0:
                print("You have not scheduled any meetings")
                employee(mydb, id)
            else:
                print("a. Edit Meeting Information")
                print("b. Add New Employee")
                print("c. Remove Employee")
                inp = input()

                if inp == 'a':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:

                        print("Current Description: " + meeting_details[0][1])
                        print("Current Date and Time: " + str(meeting_details[0][2]))
                        print()
                        print("Enter New Description (-1 for no Change): ")
                        new_description = input()
                        if (new_description == '-1'):
                            new_description = meeting_details[0][1]
                        print("Enter New Date-Time(YYYY--MM--DD HH:MM:SS) (-1 for no Change): ")
                        new_time = input()
                        if new_time == '-1':
                            new_time = meeting_details[0][2]
                        mycursor.execute(
                            'UPDATE Meetings SET purpose = "' + str(new_description) + '" WHERE id = ' + str(
                                meeting_id))
                        mydb.commit()
                        mycursor.execute(
                            'UPDATE Meetings SET date = "' + str(new_time) + '" WHERE id = ' + str(meeting_id))
                        mydb.commit()
                # added check for employee_id
                if inp == 'b':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    # added check for date in meeting
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:
                        while True:
                            print('Enter Employee ID: ')
                            emp_id = input()
                            if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                                print('Wrong Employee ID entered, enter again')
                                continue
                            break
                        mycursor.execute('SELECT * from Meetings_employee WHERE id = ' + str(
                            meeting_id) + ' and employee_id= ' + str(emp_id));

                        meeting_details = mycursor.fetchall()
                        if (len(meeting_details) == 0):
                            mycursor.execute(
                                'insert into Meetings_employee values( ' + str(meeting_id) + ', ' + str(emp_id) + ')')
                        else:
                            print("Employee Already in list")

                if (inp == 'c'):
                    print()
                    print("Enter Meeting ID: ")
                    meeting_id = input()
                    while True:
                        print('Enter Employee ID: ')
                        emp_id = input()
                        if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                            print('Wrong Employee ID entered, enter again')
                            continue
                        break
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(id)+' AND date >= \''+current_date_time+'\'');
                    meeting_details = mycursor.fetchall()
                    if (len(meeting_details) == 0):
                        print("Wrong Meeting ID")
                    else:
                        mycursor.execute(
                            'DELETE from Meetings_employee WHERE id = ' + str(meeting_id) + ' and employee_id= ' + str(
                                emp_id))
                        mydb.commit()

            employee(mydb, id)

        elif (choice == 16):

            print()
            print("Enter Employee ID: ")
            emp_id = input()
            mycursor.execute(
                'SELECT * from employee_personal_info WHERE employee_id = ' + emp_id + ' and manager_id = ' + str(id))
            data = mycursor.fetchall()

            if (len(data) == 0):
                print("Invalid Employee ID")

            else:
                mycursor.execute('SELECT * from Employee_Performance WHERE id = ' + str(emp_id));
                performance_data = mycursor.fetchall()

                print("Tasks Completed: " + str(performance_data[0][1]))
                print("Backlogs: " + str(performance_data[0][2]))
                print("Communication Skills: " + str(performance_data[0][3]))
                print("Output Quality: " + str(performance_data[0][4]))
                print("Analytic Skills: " + str(performance_data[0][5]))

                print()
                print("Update Tasks Completed (-1 for no change): ")
                new_task = input()
                if (new_task == '-1'):
                    new_task = str(performance_data[0][1])

                print("Update Backlogs (-1 for no change): ")
                new_backs = input()
                if (new_backs == '-1'):
                    new_backs = str(performance_data[0][2])

                print("Update Communication Skills (-1 for no change): ")
                new_comm = input()
                if (new_comm == '-1'):
                    new_comm = str(performance_data[0][3])

                print("Update Output Quality (-1 for no change): ")
                new_qual = input()
                if (new_qual == '-1'):
                    new_qual = str(performance_data[0][4])

                print("Update Analytic Skills (-1 for no change): ")
                new_skill = input()
                if (new_skill == '-1'):
                    new_skill = str(performance_data[0][5])

                mycursor.execute(
                    'UPDATE Employee_Performance SET task_complete = ' + str(new_task) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET backlogs = ' + str(new_backs) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET comm_skill = ' + str(new_comm) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET output_quality = ' + str(new_qual) + ' WHERE id = ' + str(emp_id))
                mydb.commit()

                mycursor.execute(
                    'UPDATE Employee_Performance SET analytic_skill = ' + str(new_skill) + ' WHERE id = ' + str(
                        emp_id))
                mydb.commit()

            employee(mydb, id)


    # user general employee
    else:
        print('1. View Information')
        print('2. View Tasks')
        print('3. Create new Task ')
        print('4. View Meetings')
        print('5. Schedule new meeting')
        print('6. Update Password')
        print('7. Update Personal Info')
        print('8. Apply for Leave')
        print('9. View leave Status')
        print('10. View all the employees')
        print('11. View all Employees of a specific Department')
        print('12. View Information of a specific Employee')
        print('13. Edit Meeting')
        print('0. Logout')

        choice = int(input())
        if choice == 0:
            login_menu(mydb)
        if choice == 1:
            view_info_employee_client.view_employee_info(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 2:
            view_all_tasks.view_tasks_employee(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 3:
            create_new_task.create_task(mydb)
            print()
            employee(mydb, id)
        elif choice == 4:
            Meetings.view_meetings(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 5:
            Meetings.call_new_meeting(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 6:
            Update_password_personalInfo.update_password(mydb, id)
            print()
            employee(mydb, id)
        elif choice == 7:
            Update_password_personalInfo.update_personal_info(mydb, id)
            employee(mydb, id)
        # Applying for leaves
        elif choice == 8:
            mycursor.execute('SELECT manager_id from employee_personal_info where employee_id = ' + str(id))
            mang_id = mycursor.fetchall()
            # Verification of Date can be done here
            print("From (YYYY--MM--DD): ")
            start_date = input()
            print("To (YYYY--MM--DD): ")
            end_date = input()
            print("Reason for leave: ")
            Reason = input()
            insert_query = 'insert into leave_request values(' + str(id) + ', ' + str(
                (mang_id[0][
                    0])) + ',  "' + start_date + '", "' + end_date + '", "' + Reason + '", 0 )'  ######## DOUBT HERE(Check reason) ####
            print(insert_query)
            mycursor.execute(insert_query);
            print("Your request has been submitted")
            mydb.commit()
            print()
            employee(mydb, id)
        # view leave status
        elif choice == 9:
            mycursor.execute('SELECT status from leave_request where employee_id = ' + str(id))
            status_val = mycursor.fetchall()
            status_val = status_val[0][0]
            if (status_val == 0):
                print("Leaves Request is pending")
            if (status_val == 1):
                print("Leaves Request is ACCEPTED")
            if (status_val == -1):
                print("Leaves Request is NOT ACCEPTED")
            employee(mydb, id)

        elif (choice == 10):
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
            employee(mydb, id)


        elif (choice == 11):
            print()
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
            employee(mydb, id)


        elif choice == 12:
            print()
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
            employee(mydb, id)


        elif choice == 13:

            print()
            # added the condition that show meeting after current date time
            mycursor.execute('SELECT count(*) from Meetings WHERE caller_id = ' + str(
                id) + ' AND date >= \'' + current_date_time + '\'')
            count_meetings = mycursor.fetchall()
            if len(count_meetings) == 0:
                print("You have not scheduled any meetings")
                employee(mydb, id)
            else:
                print("a. Edit Meeting Information")
                print("b. Add New Employee")
                print("c. Remove Employee")
                inp = input()

                if inp == 'a':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                            id) + ' AND date >= \'' + current_date_time + '\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:

                        print("Current Description: " + meeting_details[0][1])
                        print("Current Date and Time: " + str(meeting_details[0][2]))
                        print()
                        print("Enter New Description (-1 for no Change): ")
                        new_description = input()
                        if (new_description == '-1'):
                            new_description = meeting_details[0][1]
                        print("Enter New Date-Time(YYYY--MM--DD HH:MM:SS) (-1 for no Change): ")
                        new_time = input()
                        if new_time == '-1':
                            new_time = meeting_details[0][2]
                        mycursor.execute(
                            'UPDATE Meetings SET purpose = "' + str(new_description) + '" WHERE id = ' + str(
                                meeting_id))
                        mydb.commit()
                        mycursor.execute(
                            'UPDATE Meetings SET date = "' + str(new_time) + '" WHERE id = ' + str(meeting_id))
                        mydb.commit()
                # added check for employee_id
                if inp == 'b':
                    print()
                    print('Enter Meeting ID: ')
                    meeting_id = input()
                    # added check for date in meeting
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                            id) + ' AND date >= \'' + current_date_time + '\'')
                    meeting_details = mycursor.fetchall()
                    if len(meeting_details) == 0:
                        print("Wrong Meeting ID")
                    else:
                        while True:
                            print('Enter Employee ID: ')
                            emp_id = input()
                            if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                                print('Wrong Employee ID entered, enter again')
                                continue
                            break
                        mycursor.execute('SELECT * from Meetings_employee WHERE id = ' + str(
                            meeting_id) + ' and employee_id= ' + str(emp_id));

                        meeting_details = mycursor.fetchall()
                        if (len(meeting_details) == 0):
                            mycursor.execute(
                                'insert into Meetings_employee values( ' + str(meeting_id) + ', ' + str(emp_id) + ')')
                        else:
                            print("Employee Already in list")

                if (inp == 'c'):
                    print()
                    print("Enter Meeting ID: ")
                    meeting_id = input()
                    while True:
                        print('Enter Employee ID: ')
                        emp_id = input()
                        if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                            print('Wrong Employee ID entered, enter again')
                            continue
                        break
                    mycursor.execute(
                        'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                            id) + ' AND date >= \'' + current_date_time + '\'');
                    meeting_details = mycursor.fetchall()
                    if (len(meeting_details) == 0):
                        print("Wrong Meeting ID")
                    else:
                        mycursor.execute(
                            'DELETE from Meetings_employee WHERE id = ' + str(meeting_id) + ' and employee_id= ' + str(
                                emp_id))
                        mydb.commit()

            employee(mydb, id)



# employee that is not hr employee
# def normal_employee(mydb, id):
#     employee_name = Meetings.get_employee_name_given_id(mydb, id)
#     print('-------Welcome '+ employee_name + '--------')
#
#     print('8. Back')
#     print()
#     op = int(input('Enter Choice: '))
#
#     else:
#         login_menu(mydb)


# director page
def director(mydb):
  now = datetime.now()
  current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
  director_id = 0
  print('----------Welcome-----------')
  print()
  print('1. View all the Projects')
  print('2. View Information of  Employees')
  print('3. View information of a Client')
  print('4. Assign new tasks')
  print('5. Call Meeting')
  print('6. Show Meetings')
  print('7. View Company Statistics')
  print('8. Add the statistics for the year')
  print('9. Update Password')
  print('10. Update Personal Information')
  print('11. Update leave approvals')
  print('12. Edit meeting')
  print('13. Edit Task')
  print('14. Edit employee Performance')
  print('15. Back')
  print()
  mycursor = mydb.cursor()
  op = int(input('Enter Choice: '))
  if op == 1:
    view_all_tasks.view_tasks(mydb)
    director(mydb)
  elif op == 2:
    print()
    print()
    while True:
      print('a. View all the employees')
      print('b. View all Employees of a specific Department')
      print('c. View Information of a specific Employee')
      print('d. Back')
      ch = input('Enter option: ')
      if ch == 'a':
        view_info_employee_client.view_all_employee(mydb)
        print()
      elif ch == 'b':
        dept = input('Enter Department Name: ')
        while not view_info_employee_client.check_department(mydb,dept):
          dept = input('Department Name Entered Wrong, Enter Again: ')
        view_info_employee_client.view_employee_department(mydb, dept)
        print()
      elif ch == 'c':
        emp_id = int(input('Enter Employee Id: '))
        while not view_info_employee_client.check_emp_id(mydb,emp_id):
          emp_id = int(input('Employee Id entered Wrong, enter again: '))
        view_info_employee_client.view_employee_info(mydb, emp_id)
        print()
      else:
        print()
        print()
        director(mydb)
  elif op == 3:
    print()
    print()
    while True:
      print('a. View all the Clients')
      print('b. View Information of a specific Client')
      print('c. Back')
      ch = input('Enter option: ')
      if ch == 'a':
        view_info_employee_client.view_all_clients(mydb)
        print()
      elif ch == 'b':
        id = int(input('Enter Client Id: '))
        while not view_info_employee_client.check_client_id(mydb,id):
          id = int(input('Client Id entered Wrong, enter again: '))
        view_info_employee_client.view_client(mydb,id)
      else:
        print()
        print()
        director(mydb)
  elif op == 4:
    create_new_task.create_task(mydb)
    print()
    director(mydb)
  elif op == 5:
      Meetings.call_new_meeting(mydb, 0)
      print()
      director(mydb)
  elif op == 6:
    Meetings.view_meetings(mydb, 0)
    print()
    director(mydb)
  elif op == 7:
      Company_stats.view_company_stas(mydb)
      print()
      director(mydb)
  elif op == 8:
      Company_stats.add_company_stats(mydb)
      print()
      director(mydb)
  elif op == 9:
      Update_password_personalInfo.update_password(mydb, 0)
      print()
      director(mydb)
  elif op == 10:
      Update_password_personalInfo.update_personal_info(mydb, 0)
      print()
      director(mydb)
  elif op == 11:
      mycursor.execute(
          'SELECT T1.*,T2.name  FROM leave_request as T1, employee_personal_info as T2 WHERE T1.manager_id=' + str(
              director_id) + ' and T1.employee_id = T2.employee_id')
      lis_request = mycursor.fetchall()
      if len(lis_request) == 0:
          print("NO LEAVE REQUEST")
      else:
          for i in lis_request:
              print("Name: " + str(i[6]) + " Employee Id: " + str(i[0]) + " From: " + str(i[2]) + " To: " + str(
                  i[3]) + " Reason: " + str(i[4]))
          print("Update Leave Status? Y/N")
          choice = input()

          if choice == "Y" or choice == "y":
              print("Enter Employee id: ")
              emp_id = int(input())
              print("Approve? Y/N")
              choice = input()
              if choice == "Y" or choice == "y":
                  mycursor.execute('UPDATE leave_request SET status = 1 WHERE employee_id = ' + str(emp_id))
                  mydb.commit()
              else:
                  mycursor.execute('UPDATE leave_request SET status = -1 WHERE employee_id = ' + str(emp_id))
                  mydb.commit()

          else:
              pass
      mycursor.close()
      director(mydb)
  elif op == 13:
    print()
    print("a. Edit task Description")
    print("b. Add an employee to task")
    print("c. Remove an employee from task")
    inp = input()

    if inp == 'a':
      done = False
      while done == False:
          print()
          print('Enter Task ID: ')
          task_id = input()
          try:
              mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
              # temp = mycursor.fetchall()

              done = True

          except:
              print("Invalid Task ID, Please Enter Again")
      if done:
          curr_descrip = mycursor.fetchall()
          curr_descrip = curr_descrip[0][0]
          print("Current Description: " + str(curr_descrip))
          print()
          print("Enter new Description: ")
          new_description = input()
          mycursor.execute(
              'UPDATE tasks_info SET description = "' + str(new_description) + '" WHERE id = ' + str(
                  task_id))  # check new_description
          mydb.commit()
          print("Update Made")

    if inp == 'b':
      done = False
      while (done == False):
          print()
          print('Enter Task ID: ')
          task_id = input()
          try:
              mycursor.execute('SELECT description from tasks_info WHERE id = ' + str(task_id))
              temp = mycursor.fetchall()
              done = True

          except:
              print("Invalid Task ID")

      if (done):
          # check for employee ID added
          while True:
              print("Enter New Employee ID: ")
              new_emp = input()
              if not view_info_employee_client.check_emp_id(mydb, int(new_emp)):
                  print('Employee ID entered Wrong, Please Enter again')
                  print()
                  continue
              break
          mycursor.execute(' insert into tasks_employee values( ' + str(task_id) + ', ' + str(new_emp) + ')');
          mydb.commit()
          print("Update Made")

    if inp == 'c':
      # check for employee ID added
      while True:
          print("Enter Employee ID: ")
          emp = input()
          if not view_info_employee_client.check_emp_id(mydb, int(emp)):
              print('Employee ID entered Wrong, Please Enter again')
              print()
              continue
          break
      # print("Enter Employee ID: ")
      # emp = input()
      print("Enter Task ID: ")
      task_id = input()
      mycursor.execute(
          ' DELETE FROM tasks_employee WHERE employee_id = ' + str(emp) + ' and id = ' + str(task_id))
      mydb.commit()
      print("Update Made")

    mycursor.close()
    director(mydb)

  elif op == 12:

        print()
        # added the condition that show meeting after current date time
        mycursor.execute(
          'SELECT count(*) from Meetings WHERE caller_id = ' + str(director_id) + ' AND date >= \'' + current_date_time + '\'')
        count_meetings = mycursor.fetchall()
        if len(count_meetings) == 0:
          print("You have not scheduled any meetings")
          employee(mydb, id)
        else:
          print("a. Edit Meeting Information")
          print("b. Add New Employee")
          print("c. Remove Employee")
          inp = input()

          if inp == 'a':
              print()
              print('Enter Meeting ID: ')
              meeting_id = input()
              mycursor.execute(
                  'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                      director_id) + ' AND date >= \'' + current_date_time + '\'')
              meeting_details = mycursor.fetchall()
              if len(meeting_details) == 0:
                  print("Wrong Meeting ID")
              else:

                  print("Current Description: " + meeting_details[0][1])
                  print("Current Date and Time: " + str(meeting_details[0][2]))
                  print()
                  print("Enter New Description (-1 for no Change): ")
                  new_description = input()
                  if (new_description == '-1'):
                      new_description = meeting_details[0][1]
                  print("Enter New Date-Time(YYYY--MM--DD HH:MM:SS) (-1 for no Change): ")
                  new_time = input()
                  if new_time == '-1':
                      new_time = meeting_details[0][2]
                  mycursor.execute(
                      'UPDATE Meetings SET purpose = "' + str(new_description) + '" WHERE id = ' + str(
                          meeting_id))
                  mydb.commit()
                  mycursor.execute(
                      'UPDATE Meetings SET date = "' + str(new_time) + '" WHERE id = ' + str(meeting_id))
                  mydb.commit()
          # added check for employee_id
          if inp == 'b':
              print()
              print('Enter Meeting ID: ')
              meeting_id = input()
              # added check for date in meeting
              mycursor.execute(
                  'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                      director_id) + ' AND date >= \'' + current_date_time + '\'')
              meeting_details = mycursor.fetchall()
              if len(meeting_details) == 0:
                  print("Wrong Meeting ID")
              else:
                  while True:
                      print('Enter Employee ID: ')
                      emp_id = input()
                      if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                          print('Wrong Employee ID entered, enter again')
                          continue
                      break
                  mycursor.execute('SELECT * from Meetings_employee WHERE id = ' + str(
                      meeting_id) + ' and employee_id= ' + str(emp_id));

                  meeting_details = mycursor.fetchall()
                  if (len(meeting_details) == 0):
                      mycursor.execute(
                          'insert into Meetings_employee values( ' + str(meeting_id) + ', ' + str(emp_id) + ')')
                  else:
                      print("Employee Already in list")

          if (inp == 'c'):
              print()
              print("Enter Meeting ID: ")
              meeting_id = input()
              while True:
                  print('Enter Employee ID: ')
                  emp_id = input()
                  if not view_info_employee_client.check_emp_id(mydb, int(emp_id)):
                      print('Wrong Employee ID entered, enter again')
                      continue
                  break
              mycursor.execute(
                  'SELECT * from Meetings WHERE id = ' + str(meeting_id) + ' and caller_id = ' + str(
                      id) + ' AND date >= \'' + current_date_time + '\'');
              meeting_details = mycursor.fetchall()
              if (len(meeting_details) == 0):
                  print("Wrong Meeting ID")
              else:
                  mycursor.execute(
                      'DELETE from Meetings_employee WHERE id = ' + str(meeting_id) + ' and employee_id= ' + str(
                          emp_id))
                  mydb.commit()
        mycursor.close()
        director(mydb)


  elif op == 14:

      print()
      print("Enter Employee ID: ")
      emp_id = input()
      mycursor.execute(
          'SELECT * from employee_personal_info WHERE employee_id = ' +emp_id + ' and manager_id = ' + str(director_id))
      data = mycursor.fetchall()

      if (len(data) == 0):
          print("Invalid Employee ID")

      else:
          mycursor.execute('SELECT * from Employee_Performance WHERE id = ' + str(emp_id));
          print('SELECT * from Employee_Performance WHERE id = ' + str(emp_id))
          performance_data = mycursor.fetchall()

          print("Tasks Completed: " + str(performance_data[0][1]))
          print("Backlogs: " + str(performance_data[0][2]))
          print("Communication Skills: " + str(performance_data[0][3]))
          print("Output Quality: " + str(performance_data[0][4]))
          print("Analytic Skills: " + str(performance_data[0][5]))

          print()
          print("Update Tasks Completed (-1 for no change): ")
          new_task = input()
          if (new_task == '-1'):
              new_task = str(performance_data[0][1])

          print("Update Backlogs (-1 for no change): ")
          new_backs = input()
          if (new_backs == '-1'):
              new_backs = str(performance_data[0][2])

          print("Update Communication Skills (-1 for no change): ")
          new_comm = input()
          if (new_comm == '-1'):
              new_comm = str(performance_data[0][3])

          print("Update Output Quality (-1 for no change): ")
          new_qual = input()
          if (new_qual == '-1'):
              new_qual = str(performance_data[0][4])

          print("Update Analytic Skills (-1 for no change): ")
          new_skill = input()
          if (new_skill == '-1'):
              new_skill = str(performance_data[0][5])

          mycursor.execute(
              'UPDATE Employee_Performance SET task_complete = ' + str(new_task) + ' WHERE id = ' + str(emp_id))
          mydb.commit()

          mycursor.execute(
              'UPDATE Employee_Performance SET backlogs = ' + str(new_backs) + ' WHERE id = ' + str(emp_id))
          mydb.commit()

          mycursor.execute(
              'UPDATE Employee_Performance SET comm_skill = ' + str(new_comm) + ' WHERE id = ' + str(emp_id))
          mydb.commit()

          mycursor.execute(
              'UPDATE Employee_Performance SET output_quality = ' + str(new_qual) + ' WHERE id = ' + str(emp_id))
          mydb.commit()

          mycursor.execute(
              'UPDATE Employee_Performance SET analytic_skill = ' + str(new_skill) + ' WHERE id = ' + str(
                  emp_id))
          mydb.commit()

      director(mydb)

  else:
    login_menu(mydb)


# client
def client(mydb, id):
  mycursor = mydb.cursor()
  # Finding Client Name
  mycursor.execute('SELECT company_name FROM clients WHERE id= '+str(id))
  myresult = mycursor.fetchall()
  client_name = '--------Welcome '
  for x in myresult:
    client_name = client_name + x[0] +'--------------'
  print()
  print(client_name)
  print('1. Check the current projects')
  print('2. View Past projects')
  print('3: Back')
  op = int(input('Enter choice:'))
  # ch = input('Continue/Back:')

  if op == 3:
    mycursor.close()
    login_menu(mydb)
  else:
    if op == 1:
      mycursor.close()
      Client_project_info.client_project_info_current(mydb, id)
      client(mydb, id)
    elif op == 2:
      mycursor.close()
      Client_project_info.client_project_info_past(mydb, id)
      client(mydb, id)


# login into system
def login_menu(mydb):
  print('------Login-------')
  print()
  id = int(input('Enter UserId:'))
  password = input('Enter Password:')
  user = input('Enter User(Employee/Client/Director):')
  proceed = input('Continue/Back:')

  if proceed == 'Continue':
    result = Check_login_id.check_login_id(mydb, id, password, user)
    if result:
      if user == 'Employee':
        print("Login Successful")
        employee(mydb, id)
      elif user == 'Client':
        print('Login Successful')
        # print('\n'*80)
        # os.system('cls')
        client(mydb, id)
        # login_menu(mydb)
      else:
        print('Login Successful')
        director(mydb)
        # login_menu(mydb)
    else:
      print('UserId or Password Wrong')
      print('Try Again')
      login_menu(mydb)
  else:
    start_menu(mydb)


# starting menu
def start_menu(mydb):
  mycursor = mydb.cursor()
  print('------Employee Management System-------')
  print()
  print('1. Login')
  print('2. View Job Openings')
  print('3. View Workshops/Events')
  print('4. Exit')
  print()

  ch = int(input('Enter choice:'))

  if ch == 1:
    # os.system('cls')
    mycursor.close()
    login_menu(mydb)
  elif ch == 2:
    # os.system('cls')
    mycursor.close()
    View_Job_openings.view_job_openings_query(mydb)
    # os.system('cls')
    start_menu(mydb)
  elif ch == 3:
    mycursor.close()
    View_Workshops.view_workshops(mydb)
    start_menu(mydb)
  else:
    sys.exit(0)


if __name__ == '__main__':
  mydb = connect_database()
  start_menu(mydb)
