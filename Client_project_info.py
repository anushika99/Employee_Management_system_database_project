# Import Statement
from tabulate import tabulate

def client_project_info_current(mycursor,id):
    print('----------Current Projects------')
    print()
    query = 'SELECT id, description, date, status FROM tasks_info WHERE (status =\'InProgress\' OR  status = \'Ongoing\') AND id IN(SELECT task_id FROM clients_project WHERE id=' + str(id) +')'
    mycursor.execute(query)
    result_list = []
    myresult = mycursor.fetchall()
    count = 1
    task_id_list = []
    for x in myresult:
        task_id_list.append(x[0])
        tuple_list = [count, x[1], x[2],x[3]]
        count = count +1
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['S.No', 'Project Description', 'Deadline', 'Status']))
    print()