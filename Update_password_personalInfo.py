""" Update Password and Personal Info of a employee """


# update password of a employee of given id
def update_password(mydb, id):
    print('----- UPDATE PASSWORD-----')
    mycursor = mydb.cursor()
    mycursor.execute('SELECT password FROM Employee_UserID WHERE id = ' +str(id))
    myresult = mycursor.fetchall()
    for x in myresult:
        prev_conf = x[0]
    while True:
        prev = input('Enter Previous Psssword: ')
        if prev_conf != prev:
            print('Previous Password entered wrong, please enter again')
            continue
        break
    while True:
        new1 = input('Enter new password: ')
        new2 = input('Confirm new password: ')
        if new1!= new2:
            print('Passwords not match, please enter again')
            continue
        break

    query = 'UPDATE Employee_UserID SET password = \''+str(new1)+'\' WHERE id = '+str(id)
    mycursor.execute(query)
    mydb.commit()
    mycursor.close()
    print(' Password Updated')
    print()
    return


# employee updating it's address and mobile no.
def update_personal_info(mydb, id):
    mycursor = mydb.cursor()
    print('---- UPDATE PERSONAL INFORMATION ----')
    print()
    print('1. Update Address')
    print('2. Update Phone No.')
    while True:
        ch = int(input('Enter Choice: '))
        if ch == 1:
            city = input('Enter new city: ')
            state = input('Enter new state: ')
            pincode = input('Enter new pincode: ')
            addr = input('Enter the new full address: ')

            query = 'UPDATE address SET city = \''
            query = query + city + '\', state = \''
            query = query + state + '\', pincode = ' + pincode
            query = query + ', addr = \'' + addr
            query = query + '\' WHERE id = (SELECT address_id FROM employee_personal_info WHERE employee_id = '+str(id)+')'
            mycursor.execute(query)
            mydb.commit()
            print(' Address Updated')
        else:
            phone = input('Enter new Contact No.: ')
            mycursor.execute('UPDATE employee_personal_info SET phone = '+phone+' WHERE employee_id = '+ str(id))
            mydb.commit()
            print(' Phone No. Updated')
        op = input('Want to continue(Y/N): ')
        if op == 'N':
            break
    mycursor.close()
    print()
    return
