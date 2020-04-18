# Import Statements
import mysql.connector
import os
# importing python files
import View_Job_openings
import View_Workshops
import Check_login_id
import Client_project_info


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
  op = int(input('Enter choice:'))
  ch = input('Continue/Back:')

  if ch == 'Back':
    mycursor.close()
    login_menu(mydb)
  else:
    if op == 1:
      mycursor.close()
      Client_project_info.client_project_info_current(mydb, id)
      client(mydb, id)


# login into system
def login_menu(mydb):
  mycursor = mydb.cursor()
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
        print("Login")
      elif user == 'Client':
        print('Login Successful')
        # print('\n'*80)
        # os.system('cls')
        mycursor.close()
        client(mydb, id)
      else:
        print('Login Successful')
    else:
      mycursor.close()
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
    return


if __name__ == '__main__':
  mydb = connect_database()
  start_menu(mydb)
