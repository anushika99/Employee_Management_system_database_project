""" Calling and viewing meetings of an employee"""
from tabulate import tabulate
import create_new_task  # to take valid date, month, year input
import view_info_employee_client # for taking client input for new meeting entry
from datetime import datetime
import mail

# helper function - to get employee_name corresponding to employee_id
def get_employee_name_given_id(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name FROM employee_personal_info WHERE employee_id =' + str(id))
    myresult  = mycursor.fetchall()
    for x in myresult:
        return x[0]


# viewing all the meetings(that needs to attended or called) of a specific employee
def view_meetings(mydb, id):
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    mycursor = mydb.cursor()
    query = 'SELECT * FROM meetings, meetings_employee WHERE meetings.id = meetings_employee.id AND (caller_id = '+ str(id) +' OR employee_id ='+ str(id) +') AND date >=\'' + current_date_time+'\''
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

    if len(result_list) == 0:
        print('No Meeting Scheduled')
    else:
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
    attendees = ''
    for i in employee_ids:
        sql = "INSERT INTO Meetings_employee VALUES (%s,%s)"
        val = (str(meeting_id), str(i))
        mycursor.execute(sql, val)
        attendees = attendees + get_employee_name_given_id(mydb, i)+", "

    meeting_details = 'Purpose- '+purpose+' Date & Time- '+date_time_string.replace(':','-')+'  Caller- '+get_employee_name_given_id(mydb,id)
    meeting_details = meeting_details + ' Attendees- '+attendees
    print('Added new Meeting')
    mydb.commit()
    # print(meeting_details)
    for i in employee_ids:
        mail.send_notification_meetings(meeting_details, mydb, i)
    mycursor.close()
    return


def edit_meeting(mydb, id):
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    mycursor = mydb.cursor()
    # added the condition that show meeting after current date time
    mycursor.execute(
        'SELECT count(*) from Meetings WHERE caller_id = ' + str(id) + ' AND date >= \'' + current_date_time + '\'')
    count_meetings = mycursor.fetchall()
    if len(count_meetings) == 0:
        print("You have not scheduled any meetings")
        mycursor.close()
        return
    else:
        print('---Edit Meetings---')
        print("a. Edit Meeting Information")
        print("b. Add New Employee")
        print("c. Remove Employee")

        mycursor.execute('SELECT * FROM meetings, meetings_employee WHERE meetings.id = meetings_employee.id AND caller_id = '+ str(id) +' AND date >=\'' + current_date_time+'\'')
        inp = input()
        print('--Meetings scheduled by You--')
        myresult = mycursor.fetchall()
        meeting_ids = []
        result_list = []
        for x in myresult:
            if x[0] in meeting_ids:
                indx = meeting_ids.index(x[0])
                result_list[indx][4] = result_list[indx][4] + ', ' + get_employee_name_given_id(mydb, x[5])
            else:
                caller_name = get_employee_name_given_id(mydb, x[3])
                attendee_name = get_employee_name_given_id(mydb, x[5])
                meeting_ids.append(x[0])
                tuple_list = [x[0], x[1], x[2], caller_name, attendee_name]
                result_list.append(tuple_list)
        print(tabulate(result_list, headers=['Meeting_Id', 'Meeting purpose', 'Meeting date & time', 'Caller', 'Attendee']))
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

        mycursor.close()
        return
