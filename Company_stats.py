""" Viewing company stats and updating the stats of the current year by the director """
from tabulate import tabulate


# analysis of company statistics
def analysis_company_stats(mydb):
    print('----Company Statistics analysis------')
    print()
    mycursor = mydb.cursor()
    # 1. Average
    mycursor.execute('SELECT AVG(manpower), AVG(budget), AVG(expenditure), AVG(revenue) FROM company_statistics')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Average Manpower: ', x[0])
        print('Average Budget: ', x[1])
        print('Average Expenditure: ', x[2])
        print('Average Revenue: ', x[3])

    print()
    mycursor.execute('select year, revenue from company_statistics where revenue = (select max(revenue) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Maximum Revenue: ', x[1])
        print('Year of maximum Revenue: ', x[0])
    print()

    mycursor.execute('select year, revenue from company_statistics where revenue = (select min(revenue) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Minimum Revenue: ', x[1])
        print('Year of minimum Revenue: ', x[0])
    print()

    mycursor.execute('select year, manpower from company_statistics where manpower = (select max(manpower) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Maximum Manpower: ', x[1])
        print('Year of maximum Manpower: ', x[0])
    print()

    mycursor.execute('select year, manpower from company_statistics where manpower = (select min(manpower) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Minimum Manpower: ', x[1])
        print('Year of Minimum Manpower: ', x[0])
    print()

    mycursor.execute('select year, budget from company_statistics where budget = (select max(budget) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Maximum budget: ', x[1])
        print('Year of maximum budget: ', x[0])
    print()

    mycursor.execute('select year, budget from company_statistics where budget = (select min(budget) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Minimum Budget: ', x[1])
        print('Year of minimum Budget: ', x[0])
    print()

    mycursor.execute('select year, expenditure from company_statistics where expenditure = (select max(expenditure) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Maximum expenditure: ', x[1])
        print('Year of maximum expenditure: ', x[0])
    print()

    mycursor.execute('select year, expenditure from company_statistics where expenditure = (select min(expenditure) from company_statistics)')
    myresult = mycursor.fetchall()
    for x in myresult:
        print('Minimum expenditure: ', x[1])
        print('Year of minimum expenditure: ', x[0])
    print()
    mycursor.close()
    return


# view the company yearly statistics
def view_company_stas(mydb):
    print('----Yearly Company Statistics----')
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM company_statistics')
    myresult = mycursor.fetchall()
    result_list = []
    for x in myresult:
        tuple_list = [x[0], x[1], x[2], x[3], x[4]]
        result_list.append(tuple_list)
    print(tabulate(result_list, headers=['Year', 'Manpower', 'Budget', 'Expenditure', 'Revemue']))
    print()
    ch = input('See the analysis of data(Y/N): ')
    mycursor.close()
    if ch == 'Y':
        analysis_company_stats(mydb)
    return


# add the yearly company statistics
def add_company_stats(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT year FROM company_statistics ORDER BY year DESC Limit 1')
    myresult = mycursor.fetchall()
    for x in myresult:
        last_year = x[0]
    while True:
        year = input('Enter Year(last year = ' + str(last_year)+': ')
        if not year.isnumeric():
            print('Wrong year entered, try again')
            continue
        break
    while True:
        if int(year) != last_year+1:
            print('Year should next year to last year, enter again')
            continue
        break
    while True:
        manpower = input('Enter Manpower: ')
        if not manpower.isnumeric():
            print('Manpower entered wrong, enter again')
            continue
        break
    while True:
        budget = input('Enter Budget: ')
        if not budget.isnumeric():
            print('Budget entered wrong, enter again')
            continue
        break
    while True:
        expenditure = input('Enter Expenditure: ')
        if not expenditure.isnumeric():
            print('Expenditure entered wrong, enter again')
            continue
        break
    while True:
        revenue = input('Enter Revenue: ')
        if not revenue.isnumeric():
            print('Revenue entered wrong, enter again')
            continue
        break

    sql = 'INSERT into company_statistics VALUES(%s, %s, %s, %s, %s)'
    val = (year, manpower, budget, expenditure, revenue)
    mycursor.execute(sql,val)
    print('Added the yearly statistics')
    print()
    mydb.commit()
    mycursor.close()
    return
