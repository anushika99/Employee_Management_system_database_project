import string
import random


def add_employee(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT employee_id FROM employee_personal_info ORDER BY employee_id DESC Limit 1');
    last_id = mycursor.fetchall()
    last_id = int(last_id[0][0]) + 1
    # print(last_id)
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

        mycursor.execute('SELECT id FROM address ORDER BY id DESC Limit 1')
        last_addr_id = mycursor.fetchall()
        last_addr_id = int(last_addr_id[0][0]) + 1

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

    print('Enter email id: ')
    email = input()

    mycursor.execute(
        'insert into employee_personal_info values( ' + str(last_id) + ', "' + str(name) + '", ' + str(
            age) + ', "' + str(gender) + '", ' + str(last_addr_id) + ', ' + str(phone) + ', ' + str(
            yoj) + ', ' + str(salary) + ', ' + str(mang_id) + ', "' + str(desig) + '", ' + str(
            dept) + ', 0, 0)');
    mydb.commit()
    letters = string.ascii_lowercase
    passkey = ''.join(random.choice(letters) for i in range(10))
    mycursor.execute('insert into Employee_UserId values( ' + str(last_id) + ', "' + str(passkey) + '")')
    mycursor.execute('insert into Employee_Performance values(' + str(last_id) + ', 0, 0, 0, 0, 0)')
    mycursor.execute('insert into email_id values (%s,%s)', (str(last_id), email))
    mydb.commit()
    mycursor.close()
    return


def delete_employee(mydb):
    mycursor = mydb.cursor()
    print()
    print("Enter Employee ID: ")
    emp_id = input()
    mycursor.execute('SELECT manager_id FROM employee_personal_info WHERE employee_id = ' + emp_id)
    myresult = mycursor.fetchall()
    manager_id = myresult[0][0]
    mycursor.execute('SELECT employee_id FROM employee_personal_info WHERE manager_id = ' + emp_id)
    myresult = mycursor.fetchall()
    for x in myresult:
        mycursor.execute(
            'UPDATE employee_personal_info SET manager_id = ' + str(manager_id) + ' WHERE employee_id =  ' + str(x[0]))
        # mydb.commit()
    mycursor.execute('SELECT intern_id FROM Intern WHERE manager_id = ' + emp_id)
    myresult = mycursor.fetchall()
    for x in myresult:
        mycursor.execute('UPDATE Intern SET manager_id = ' + str(manager_id) + ' WHERE intern_id = ' + str(x[0]))
        # mydb.commit()

    mycursor.execute('DELETE FROM leave_request WHERE employee_id = ' + emp_id)
    mycursor.execute('UPDATE leave_request SET manager_id = ' + str(manager_id) + ' WHERE manager_id = ' + emp_id)
    mycursor.execute('DELETE FROM Employee_Performance WHERE id = ' + emp_id)
    mycursor.execute('DELETE FROM Employee_UserID WHERE id = ' + emp_id)
    mycursor.execute('DELETE FROM tasks_employee WHERE employee_id = ' + emp_id)
    mycursor.execute('DELETE FROM Meetings_employee WHERE employee_id = ' + emp_id)
    mycursor.execute('DELETE FROM Meetings WHERE caller_id = ' + emp_id)
    mycursor.execute('SELECT address_id FROM employee_personal_info WHERE employee_id = '+emp_id)
    myresult = mycursor.fetchall()
    mycursor.execute('DELETE FROM email_id WHERE id = '+str(emp_id))
    mycursor.execute('DELETE FROM employee_personal_info WHERE employee_id = ' + str(emp_id))
    mycursor.execute('DELETE FROM address WHERE id = '+ str(myresult[0][0]))
    mydb.commit()
    mycursor.close()
    return