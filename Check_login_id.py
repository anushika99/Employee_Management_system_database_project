
def check_login_id(mydb, id, password, user):
    mycursor = mydb.cursor()
    if user == 'Director':
        mycursor.execute("SELECT password FROM Employee_UserId WHERE id = 0")
        myresult = mycursor.fetchall()
        mycursor.close()
        for x in myresult:
            paswrd = x[0]
        if id == 0 and password == paswrd:
            return True
        else:
            return False
    elif user == 'Employee':
        mycursor.execute("SELECT * FROM Employee_UserId")
        myresult = mycursor.fetchall()
        mycursor.close()
        for x in myresult:
            if x[0] == id and x[1] == password:
                return True
        return False
    else:
        mycursor.execute("SELECT * FROM Client_UserId")
        myresult = mycursor.fetchall()
        mycursor.close()
        for x in myresult:
            if x[0] == id and x[1] == password:
                return True
        return False


