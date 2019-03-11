from Classes.admin import *
from Dashboard.admin_dashboard import *


def log_in():
    print('--- ADMIN LOG IN ---')
    username = input('Username: ')
    flag = 1

    for anadmin in Admin.objects:
        if username.lower() == anadmin.username.lower():
            password = input('Password: ')
            flag, countdown = 0, 2
            while countdown >= 0:
                if anadmin.password == password:
                    welcome_screen(anadmin)
                    return
                else:
                    print(f'Wrong password. Attempts remaining {countdown + 1}')
                    countdown -= 1
                password = input("Password: ")
            print("Banned from the system.")

    if flag:
        ans = input((f'Admin with {username} username does not exist.\nCreate account? (y/n): '))
        if ans.lower() not in ('n', 'N'):
            sign_up()
        else:
            print('Goodbye!')


def sign_up():
    name = input('Name: \n')
    email = email_check()
    password = input('Password: \n')
    country=input('Country: \n')
    
    anadmin = Admin(name=name, email=email, password=password, country=country, city=city, available_rooms=av_rooms,pernightcost=pernightcost)
    anadmin.save()
    print('Admin account for {anadmin.name} Admin created successfully!')


def email_check():
    flag = 1
    email = input("Email: ")
    while True:
        flag = 0
        for smth in Admin.objects.only('email'):
            if smth.email == email:
                email, flag = input(f"{email} already in use. Try a different one: "), 1
                break
        if not flag:
            break
    return email