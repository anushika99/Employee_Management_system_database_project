# Import Statements
import mysql.connector
# importing python files
import View_Job_openings


# connecting to mysql database
# run command pip install mysql-connector-python to use the default caching_sha2_password plugin
def connect_database():
  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='anushi123',
    database='dbms_project'
  )
  return mydb


# starting menu
def start_menu(mycursor):

  print()
  print('1. Login')
  print('2. View Job Openings')
  print('3. View Workshops/Events')
  print('4. Exit')
  print()

  ch = int(input('Enter choice:'))

  if ch == 1:
    print('Login')
  elif ch == 2:
    View_Job_openings.view_job_openings_query(mycursor)
    start_menu(mycursor)
  elif ch == 3:
    print()
  else:
    return


if __name__ == '__main__':
  mydb = connect_database()
  mycursor = mydb.cursor()
  print('------Employee Management System-------')
  print()
  start_menu(mycursor)
