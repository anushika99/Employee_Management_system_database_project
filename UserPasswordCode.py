import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

if __name__ =='__main__':
    main_String = 'insert into Employee_UserId values'
    for i in range(50):
        f_str = '(' + str(i)+ ',"' + randomString(10)+'");'
        print(main_String+f_str)