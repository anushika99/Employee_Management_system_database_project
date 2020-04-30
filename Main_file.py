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
import view_intern_table
import leaves
import employee_view_other_employees
import edit_task
import Update_employee_performance
import employee_add_delete
import client_add_delete
import add_job_workshop

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
        print('19. View all the interns')
        print('20. Add new event')
        print('21. Add new Job opening')
        print('0. Logout')

        choice = int(input())

        if choice == 0:
            login_menu(mydb)
        elif choice == 20:
            add_job_workshop.add_workshop_event(mydb)
            print()
            employee(mydb, id)
        elif choice == 21:
            add_job_workshop.add_job_opening(mydb)
            print()
            employee(mydb, id)
        elif choice == 19:
            view_intern_table.view_interns(mydb)
            print()
            employee(mydb, id)
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
            leaves.view_leave_requests(mydb, id)
            employee(mydb, id)
        # Applying for leaves
        elif choice == 9:
            leaves.apply_for_laves(mydb, id)
            print()
            employee(mydb,id)
        # view leave status
        elif choice == 10:
            leaves.check_leave_status(mydb, id)
            print()
            employee(mydb, id)
        # viewing all the employees
        elif choice == 11:
            employee_view_other_employees.hr_all_employees(mydb)
            print()
            employee(mydb, id)
        # Viewing all the employees of a specific department
        elif choice == 12:
            print()
            employee_view_other_employees.hr_employee_dept(mydb)
            print()
            employee(mydb, id)

        # View information of a specifc employee
        elif choice == 13:
            print()
            employee_view_other_employees.hr_view_specific_employee(mydb)
            print()
            employee(mydb, id)

        # Edit task
        elif choice == 14:
            edit_task.edit_task(mydb)
            print()
            employee(mydb, id)

        elif choice == 15:
            Meetings.edit_meeting(mydb, id)
            print()
            employee(mydb, id)
        elif (choice == 16):
            Update_employee_performance.update_performance(mydb,id)
            print()
            employee(mydb, id)

        elif (choice == 17):
            print()
            print("Enter Choice (Add/Remove): ")
            val = input()
            val = (val.lower())

            if (val == 'add'):
                employee_add_delete.add_employee(mydb)
            else:
                employee_add_delete.delete_employee(mydb)
            print()
            employee(mydb, id)

        elif choice == 18:
            print()
            print("Enter Choice (Add/Remove): ")
            val = input()
            val = (val.lower())

            if (val == 'add'):
                client_add_delete.add_client(mydb)

            else:
                client_add_delete.delete_client(mydb)
            print()
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
        print('17. View all the interns')
        print('0. Logout')

        choice  = int(input('Enter Choice'))
        if choice == 0:
            login_menu(mydb)
        elif choice == 17:
            view_intern_table.view_interns(mydb)
            print()
            employee(mydb, id)
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
        if choice == 8:
            leaves.view_leave_requests(mydb, id)
            print()
            employee(mydb, id)

        # Applying for leaves
        elif choice == 9:
            leaves.apply_for_laves(mydb, id)
            print()
            employee(mydb, id)
        # view leave status
        elif choice == 10:
            leaves.check_leave_status(mydb, id)
            print()
            employee(mydb, id)

        elif (choice == 11):
            employee_view_other_employees.view_all_employees(mydb)
            print()
            employee(mydb, id)
        elif (choice == 12):
            print()
            employee_view_other_employees.view_employee_dept(mydb)
            employee(mydb, id)
        elif choice == 13:
            print()
            employee_view_other_employees.view_specific_employee(mydb)
            employee(mydb, id)

        # Edit task
        elif choice == 14:
            edit_task.edit_task(mydb)
            employee(mydb, id)

        elif choice == 15:
            Meetings.edit_meeting(mydb, id)
            print()
            employee(mydb, id)

        elif (choice == 16):
            Update_employee_performance.update_performance(mydb, id)
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
        print('14. View all the interns')
        print('0. Logout')

        choice = int(input())
        if choice == 0:
            login_menu(mydb)
        if choice == 14:
            view_intern_table.view_interns(mydb)
            print()
            employee(mydb,id)
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
            leaves.apply_for_laves(mydb, id)
            employee(mydb, id)
        # view leave status
        elif choice == 9:
            leaves.check_leave_status(mydb, id)
            employee(mydb, id)
        elif (choice == 10):
            employee_view_other_employees.view_all_employees(mydb)
            employee(mydb, id)
        elif (choice == 11):
            employee_view_other_employees.view_employee_dept(mydb)
            employee(mydb, id)
        elif choice == 12:
            employee_view_other_employees.view_specific_employee(mydb)
            employee(mydb, id)
        elif choice == 13:
            Meetings.edit_meeting(mydb, id)
            employee(mydb, id)


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
      leaves.view_leave_requests(mydb, 0)
      director(mydb)
  elif op == 13:
      edit_task.edit_task(mydb)
      director(mydb)
  elif op == 12:
      Meetings.edit_meeting(mydb, 0)
      director(mydb)
  elif op == 14:
      Update_employee_performance.update_performance(mydb, 0)
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
