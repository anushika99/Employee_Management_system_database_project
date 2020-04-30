import create_new_task


def add_workshop_event(mydb):
    mycursor = mydb.cursor()
    print('--- Add Workshop/Event---')
    name = input('Enter event name: ')
    desc = input('Enter event description: ')
    print('Enter event date')
    date = create_new_task.date_final()
    q = 'INSERT INTO workshop_event VALUES(%s,%s,%s)'
    v = (name, desc, date)
    mycursor.execute(q,v)
    mydb.commit()
    mycursor.close()
    print('Added Workshop/Event')
    return


def add_job_opening(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT count(*) FROM opening')
    myresult = mycursor.fetchall()
    new_id = myresult[0][0]
    profile = input('Enter job Profile: ')
    desc = input('Enter job description: ')
    exp = input('Enter job experience: ')
    while True:
        sal = input('Enter salary: ')
        if sal.isnumeric():
            break
        print('Salary Entered Wrong, enter again')
    skill = input('Enter Skills: ')
    query = 'INSERT INTO opening VALUES(' + str(new_id) + ',\'' + str(profile) + '\',\'' + str(desc) + '\',\'' +str(skill)+'\',\''+str(exp)+'\','+str(sal)+')'
    # print(query)
    mycursor.execute(query)
    mydb.commit()
    mycursor.close()
    print('Added Job opening')
    return
