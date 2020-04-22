# Import Statements
import mysql.connector
import os

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


# employee that is not hr employee
def normal_employee(mydb, id):
    employee_name = Meetings.get_employee_name_given_id(mydb, id)
    print('-------Welcome '+ employee_name + '--------')
    print('1. View Information')
    print('2. View Tasks')
    print('3. Create new Task ')
    print('4. View Meetings')
    print('5. Schedule new meeting')
    print('6. Update Password')
    print('7. Update Personal Info')
    print('8. Back')
    print()
    op = int(input('Enter Choice: '))
    if op == 1:
        view_info_employee_client.view_employee_info(mydb, id)
        print()
        normal_employee(mydb, id)
    elif op == 2:
        view_all_tasks.view_tasks_employee(mydb, id)
        print()
        normal_employee(mydb ,id)
    elif op == 3:
        create_new_task.create_task(mydb)
        print()
        normal_employee(mydb, id)
    elif op == 4:
        Meetings.view_meetings(mydb,id)
        print()
        normal_employee(mydb, id)
    elif op == 5:
        Meetings.call_new_meeting(mydb, id)
        print()
        normal_employee(mydb,id)
    elif op == 6:
        Update_password_personalInfo.update_password(mydb, id)
        print()
        normal_employee(mydb, id)
    elif op == 7:
        Update_password_personalInfo.update_personal_info(mydb, id)
    else:
        login_menu(mydb)


# director page
def director(mydb):
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
  print('11. Back')
  print()
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
        ######
        # TODO - check for hr employee and normal employee to be done here
        ######
        normal_employee(mydb, id)
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
