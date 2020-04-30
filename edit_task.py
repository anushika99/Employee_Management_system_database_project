import view_info_employee_client

def edit_task(mydb):
    mycursor = mydb.cursor()
    print('--- Edit Task----')
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
            mycursor.execute('SELECT employee_id FROM tasks_employee WHERE id = ' + task_id)
            myresult = mycursor.fetchall()
            # print(myresult)
            flag = False
            for x in myresult:
                if x[0] == int(new_emp):
                    flag = True
                    break
            if flag:
                print('Employee already working on the task')
            else:
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
        mycursor.execute('SELECT employee_id FROM tasks_employee WHERE id = ' + task_id)
        myresult = mycursor.fetchall()
        # print(myresult)
        flag = False
        for x in myresult:
            if x[0] == int(emp):
                flag = True
                break
        if flag:
            mycursor.execute(
                ' DELETE FROM tasks_employee WHERE employee_id = ' + str(emp) + ' and id = ' + str(task_id))
            mydb.commit()
            print("Update Made")
        else:
            print('Employee not working on this task')
    mycursor.close()
    return

