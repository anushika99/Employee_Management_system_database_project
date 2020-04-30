from tabulate import tabulate

def view_leave_requests(mydb, id):
    mycursor = mydb.cursor()
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
        mycursor.close()
        return


def apply_for_laves(mydb, id):
    mycursor = mydb.cursor()
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
    # print(insert_query)
    mycursor.execute(insert_query);
    print("Your request has been submitted")
    mydb.commit()
    mycursor.close()
    print()
    return


def check_leave_status(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * from leave_request where employee_id = ' + str(id))
    status_val = mycursor.fetchall()
    result_list =[]
    for x in status_val:
        tuple_list= [x[2], x[3], x[4]]
        if (x[5] == 0):
            tuple_list.append("Leaves Request is pending")
        if (x[5] == 1):
            tuple_list.append("Leaves Request is ACCEPTED")
        if (x[5] == -1):
            tuple_list.append("Leaves Request is NOT ACCEPTED")
        result_list.append(tuple_list)
    mycursor.close()
    if len(result_list) == 0:
        print('No leave requests')
        return
    print(tabulate(result_list, headers=['StartDate', 'End Date. ', 'Reason', 'Status']))
    return
