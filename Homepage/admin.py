from Classes.admin import *
from Dashboard.admin_dashboard import *
from Update_DB.update_db import * #welcome_screen


def log_in():
    print('--- ADMIN LOG IN ---')
    username = input('Username: ')
    flag = 1

    #add while True
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
    name = input('Name: ')
    gender=gender_check()
    email = email_check()
    username=username_check()
    password = password_check()
    country=input('Country: ')
    
    update_db_add_application(name,gender,email,username,password,country)
    print(f'Your application for administrator account has been submitted successfully!\nYou\'ll be notified via email')


def email_check():
    flag = 1
    email = input("Email: ")
    while True:
        flag = 0
        if Admin.objects(email=email):
            email, flag = input(f"{email} already in use. Try a different one: "), 1
            break
        if not flag:
            break
    return email

def username_check():
    flag=1
    username=input("Username: ")
    while True:
        flag=0
        if Admin.objects(username=username):
            username,flag=input(f"{username} already in use. Try a different one: "),1
            break
        if not flag:
            break
    return username

def password_check():
    password=input('Please type in your password: ')

    password2=input('Retype your new password: ')
    while password!=password2:
        password2=input('Passwords must match!\nTry again: ')
    return password

def gender_check():
    fixed='Select a gender:\nMale: 1\nFemale: 2\nOther: 3'
    ans=int(input(f'{fixed}\nChoice: '))
    while ans not in range(1,4):
        ans=int(input(f'Please type in an integer from 1 to 3\n{fixed}\nChoice: '))
   
    return gender_options[ans-1]