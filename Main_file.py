# Import Statements
import mysql.connector
# importing python files
import View_Job_openings
import View_Workshops
import Check_login_id


# connecting to mysql database
# run command pip install mysql-connector-python to use the default caching_sha2_password plugin
def connect_database():
  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pass',
    database='dbms_project'
  )
  return mydb


# login into system
def login_menu(mycursor):

  print('------Login-------')
  print()
  id = int(input('Enter UserId:'))
  password = input('Enter Password:')
  user = input('Enter User(Employee/Client/Director):')
  proceed = input('Continue/Back:')

  if proceed == 'Continue':
    result = Check_login_id.check_login_id(mycursor, id, password, user)
    if result:
      print('Login Successful')
    else:
      print('UserId or Password Wrong')
      print('Try Again')
      login_menu(mycursor)
  else:
    start_menu(mycursor)


# starting menu
def start_menu(mycursor):

  print('------Employee Management System-------')
  print()
  print('1. Login')
  print('2. View Job Openings')
  print('3. View Workshops/Events')
  print('4. Exit')
  print()

  ch = int(input('Enter choice:'))

  if ch == 1:
    login_menu(mycursor)
  elif ch == 2:
    View_Job_openings.view_job_openings_query(mycursor)
    start_menu(mycursor)
  elif ch == 3:
    View_Workshops.view_workshops(mycursor)
    start_menu(mycursor)
  else:
    return


if __name__ == '__main__':
  mydb = connect_database()
  mycursor = mydb.cursor()
  start_menu(mycursor)
