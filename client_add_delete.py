import string
import random


def add_client(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT id FROM clients ORDER BY id DESC Limit 1');
    last_id = mycursor.fetchall()
    last_id = int(last_id[0][0]) + 1

    print("Create New Address? (Y/N)")
    addr_stat = input()
    last_addr_id = 0;
    if ((addr_stat.lower()) == 'y'):
        print("Enter City: ")
        city = input()
        print("Enter State: ")
        state = input()
        print("Enter Pincode: ")
        pin = input()
        print("Enter Address: ")
        addr = input()

        mycursor.execute('SELECT id FROM address ORDER BY id DESC Limit 1');
        last_addr_id = mycursor.fetchall()
        last_addr_id = int(last_addr_id[0][0]) + 1

        mycursor.execute(
            'insert into address values(' + str(last_addr_id) + ', "' + str(city) + '", "' + str(
                state) + '", "' + str(pin) + '", "' + str(addr) + '")');
        mydb.commit()

    else:
        print()
        print("Enter Address ID: ")
        last_addr_id = input();

    print()
    print("Enter Client Name: ")
    name = input()
    print("Enter Client Phone: ")
    phone = input()

    mycursor.execute('insert into clients values( ' + str(last_id) + ', "' + str(name) + '", ' + str(
        last_addr_id) + ', ' + str(phone) + ')');
    mydb.commit()

    letters = string.ascii_lowercase
    passkey = ''.join(random.choice(letters) for i in range(10))
    mycursor.execute('insert into Client_UserId values( ' + str(last_id) + ', "' + str(passkey) + '")')
    mydb.commit()
    mycursor.close()
    return


def delete_client(mydb):
    mycursor = mydb.cursor()
    print()
    print("Enter Client ID: ")
    client_id = input()
    mycursor.execute('DELETE FROM clients_project WHERE id = ' + client_id)
    mycursor.execute('DELETE FROM Client_UserId WHERE id = ' + str(client_id))
    # mydb.commit()
    mycursor.execute('SELECT company_address_id FROM clients WHERE id = ' + client_id)
    myresult = mycursor.fetchall()
    mycursor.execute('DELETE FROM clients WHERE id = ' + str(client_id))
    mycursor.execute('DELETE FROM address WHERE id = ' + str(myresult[0][0]))
    mydb.commit()
    mycursor.close()
    return

