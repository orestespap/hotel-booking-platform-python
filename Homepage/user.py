from Classes.customer import *
from Dashboard.user_dashboard import *


def log_in():
    print('--- USER LOG IN ---')
    username = input('Username: ')
    password = input('Password: ')
    flag = 1

    for acustomer in Customer.objects:
        if username.lower() == acustomer.username.lower():
            flag, countdown = 0, 2
            while countdown >= 0:
                if acustomer.password == password:
                    welcome_screen(acustomer)
                    return
                else:
                    print(f'Wrong password. Attempts remaining {countdown + 1}')
                    countdown -= 1
                password = input("Password: ")
            print("Banned from the system.")

    if flag:
        ans = input((f'Account with {username} username does not exist.\nCreate account? (y/n): '))
        if ans.lower() not in ('n', 'N'):
            sign_up()
        else:
            print('Goodbye!')

def sign_up():
    name=input('Name: \n')
    email= email_check()
    username=username_check()
    password= input('Password: \n')
    gender=gender_check()
    

    customer=Customer(name=name,email=email,password=password,gender=gender,username=username)
    customer.save()
    print('Account created successfully!')

def email_check():
    
    flag=1
    email=input("Email: ")
    while True:
        flag=0
        for smth in Customer.objects.only('email'):
            if smth.email==email:
                email,flag=input(f"{email} already in use. Try a different one: "),1
                break
        if not flag:
            break
    return email

def username_check():
    flag=1
    username=input("Username: ")
    while True:
        flag=0
        for smth in Customer.objects.only('username'):
            if smth.username==username:
                username,flag=input(f"{username} already in use. Try a different one: "),1
                break
        if not flag:
            break
    return username

def gender_check():
    gender=input(f'Gender {gender_options}: \n')
    while gender.lower() not in gender_options:
        gender=input(f'Select one of the three: {gender_options}\n')
    return gender