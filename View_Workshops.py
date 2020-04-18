# Import Statement
from tabulate import tabulate


def view_workshops(mydb):
    mycursor = mydb.cursor()
    print('------Workshops/Events --------')
    print()
    mycursor.execute("SELECT * FROM workshop_event")
    result_list =[]
    myresult = mycursor.fetchall()
    count = 1
    for x in myresult:
        tuple_list = [count, x[0], x[1], x[2]]
        count = count + 1
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Event Name', 'Description', 'Date']))
    print()
    mycursor.close()
