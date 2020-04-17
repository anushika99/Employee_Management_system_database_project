
def check_login_id(mycursor, id, password, user):
    if user == 'Director':
        if id == 0 and password == 'wljbtgmymi':
            return True
        else:
            return False
    elif user == 'Employee':
        mycursor.execute("SELECT * FROM Employee_UserId")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == id and x[1] == password:
                return True
        return False
    else:
        mycursor.execute("SELECT * FROM Client_UserId")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == id and x[1] == password:
                return True
        return False


