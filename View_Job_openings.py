# Import Statement
from tabulate import tabulate


def view_job_openings_query(mycursor):
    print('------Job Openings --------')
    print()
    mycursor.execute("SELECT * FROM opening")
    result_list =[]
    myresult = mycursor.fetchall()
    for x in myresult:
        tuple_list = [x[0],x[1],x[2],x[3],x[4],x[5]]
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Job Designation', 'Description', 'Skills Required', 'Experience', 'Salary']))
    print()

