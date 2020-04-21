""" Calling and viewing meetings of an employee"""
from tabulate import tabulate
import create_new_task  # to take valid date, month, year input
import view_info_employee_client # for taking client input for new meeting entry


# helper function - to get employee_name corresponding to employee_id
def get_employee_name_given_id(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name FROM employee_personal_info WHERE employee_id =' + str(id))
    myresult  = mycursor.fetchall()
    for x in myresult:
        return x[0]


# viewing all the meetings(that needs to attended or called) of a specific employee
def view_meetings(mydb, id):
    mycursor = mydb.cursor()
    query = 'SELECT * FROM meetings, meetings_employee WHERE meetings.id = meetings_employee.id AND (caller_id = '+ str(id) +' OR employee_id ='+ str(id) +')'
    print(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mycursor.close()
    meeting_ids = []
    result_list =[]
    for x in myresult:
        if x[0] in meeting_ids:
            indx = meeting_ids.index(x[0])
            result_list[indx][4] = result_list[indx][4] + ', ' + get_employee_name_given_id(mydb, x[5])
        else:
            caller_name = get_employee_name_given_id(mydb, x[3])
            attendee_name = get_employee_name_given_id(mydb, x[5])
            meeting_ids.append(x[0])
            tuple_list  = [x[0], x[1], x[2], caller_name, attendee_name]
            result_list.append(tuple_list)

    print('Total no. of Meetings: ' + str(len(result_list)))
    print(tabulate(result_list, headers=['Meeting_Id', 'Meeting purpose', 'Meeting date & time', 'Caller', 'Attendee']))
    print()
    return


# takes input of time for meeting
def input_time():
    while True:
        time = input('Enter time in 24 hours format(hh:mm:ss): ')
        hours = time[0:2]
        if hours.isnumeric() == False:
            print('Date entered is wrong, please try again ')
            continue
        hours = int(hours)
        if hours < 0 or hours> 23:
            print('Date entered is wrong, please try again ')
            continue
        minutes = time[3:5]
        if minutes.isnumeric() == False:
            print('Date entered is wrong, please try again ')
            continue
        minutes = int(minutes)
        if minutes <0 or minutes >60 :
            print('Date entered is wrong, please try again ')
            continue
        seconds = time[6:]
        if seconds.isnumeric() == False:
            print('Date entered is wrong, please try again ')
            continue
        seconds = int(seconds)
        if seconds < 0 or seconds > 60:
            print('Date entered is wrong, please try again ')
            continue
        break
    return time


# create a new meeting entry in meetings and meetings_employee table
def call_new_meeting(mydb, id):
    mycursor = mydb.cursor()
    purpose = input('Enter meeting purpose: ')
    print('Input Date of meeting - ')
    month = create_new_task.monthinput()
    year = create_new_task.yearinput()
    date = create_new_task.dateinput(month, year)
    print('Input Time of meeting - ')
    time = input_time()
    date_time_string = year +'-'+month+'-'+date+' '+time

    # finding the id value of last meeting
    mycursor.execute('SELECT count(*) FROM Meetings')
    myresult = mycursor.fetchall()
    for x in myresult:
        meeting_id = x[0]

    # entering the employees to call in the meeting
    print('All the employees ( To select the employee_id')
    view_info_employee_client.view_all_employee(mydb)
    employee_ids =[]
    while True:
        emp_id = int(input('Enter Employee Id: '))
        if not view_info_employee_client.check_emp_id(mydb,emp_id):
            print('Employee Id entered wrong, please enter again ')
            continue
        employee_ids.append(emp_id)
        ch = input('Want to enter another employee id (Y/N): ')
        if ch == 'N':
            break

    sql = "INSERT INTO Meetings VALUES (%s,%s,%s,%s)"
    val = (str(meeting_id), purpose, date_time_string, str(id))
    mycursor.execute(sql, val)
    for i in employee_ids:
        sql = "INSERT INTO Meetings_employee VALUES (%s,%s)"
        val = (str(meeting_id), str(i))
        mycursor.execute(sql, val)
    print('Added new Meeting')
    mydb.commit()
    mycursor.close()
    return
