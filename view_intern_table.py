
from tabulate import tabulate


def view_interns(mydb):
	mycursor = mydb.cursor()
	print('------Interns Information --------')
	print()
	mycursor.execute("SELECT * FROM intern")
	result_list =[]
	myresult = mycursor.fetchall()
	count = 1
	for x in myresult:
	    tuple_list = [count, x[0], x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]]
	    count = count + 1
	    result_list.append(tuple_list)
	print(tabulate(result_list, headers=['S.No','intern id', 'Name', 'gender', 'address Id','phone number','start date','end date','stipend',' manager id','task id']))
	print()
	mycursor.close()
	return
