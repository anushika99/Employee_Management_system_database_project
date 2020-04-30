from tabulate import tabulate

def update_performance(mydb, id):
    mycursor = mydb.cursor()
    print()
    print('---Update Performance----')
    print('Employees Under me:')
    mycursor.execute('SELECT employee_id, name from employee_personal_info WHERE manager_id = ' + str(id))
    data = mycursor.fetchall()
    result =[]
    for x in data:
        result.append([x[0], x[1]])
    print(tabulate(result,  headers=['Employee Id', 'Name']))
    print("Enter Employee ID: ")
    emp_id = input()
    mycursor.execute(
        'SELECT * from employee_personal_info WHERE employee_id = ' + str(emp_id) + ' and manager_id = ' + str(id))
    data = mycursor.fetchall()

    if (len(data) == 0):
        print("Invalid Employee ID")

    else:
        mycursor.execute('SELECT * from Employee_Performance WHERE id = ' + str(emp_id));
        performance_data = mycursor.fetchall()

        print("Tasks Completed: " + str(performance_data[0][1]))
        print("Backlogs: " + str(performance_data[0][2]))
        print("Communication Skills: " + str(performance_data[0][3]))
        print("Output Quality: " + str(performance_data[0][4]))
        print("Analytic Skills: " + str(performance_data[0][5]))

        print()
        print("Update Tasks Completed (-1 for no change): ")
        new_task = input()
        if (new_task == '-1'):
            new_task = str(performance_data[0][1])

        print("Update Backlogs (-1 for no change): ")
        new_backs = input()
        if (new_backs == '-1'):
            new_backs = str(performance_data[0][2])

        print("Update Communication Skills (-1 for no change): ")
        new_comm = input()
        if (new_comm == '-1'):
            new_comm = str(performance_data[0][3])

        print("Update Output Quality (-1 for no change): ")
        new_qual = input()
        if (new_qual == '-1'):
            new_qual = str(performance_data[0][4])

        print("Update Analytic Skills (-1 for no change): ")
        new_skill = input()
        if (new_skill == '-1'):
            new_skill = str(performance_data[0][5])

        mycursor.execute(
            'UPDATE Employee_Performance SET task_complete = ' + str(new_task) + ' WHERE id = ' + str(emp_id))
        mydb.commit()

        mycursor.execute(
            'UPDATE Employee_Performance SET backlogs = ' + str(new_backs) + ' WHERE id = ' + str(emp_id))
        mydb.commit()

        mycursor.execute(
            'UPDATE Employee_Performance SET comm_skill = ' + str(new_comm) + ' WHERE id = ' + str(emp_id))
        mydb.commit()

        mycursor.execute(
            'UPDATE Employee_Performance SET output_quality = ' + str(new_qual) + ' WHERE id = ' + str(emp_id))
        mydb.commit()

        mycursor.execute(
            'UPDATE Employee_Performance SET analytic_skill = ' + str(new_skill) + ' WHERE id = ' + str(
                emp_id))
        mydb.commit()
    print('Update Done')
    mycursor.close()
    return

