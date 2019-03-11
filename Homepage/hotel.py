from Classes.hotel import *
from Dashboard.hotel_dashboard import *


def log_in():
    print('--- HOTEL LOG IN ---')
    email = input('Email: ')
    flag = 1

    for ahotel in Hotel.objects:
        if email.lower() == ahotel.email.lower():
            password = input('Password: ')
            flag, countdown = 0, 2
            while countdown >= 0:
                if ahotel.password == password:
                    welcome_screen(ahotel)
                    return
                else:
                    print(f'Wrong password. Attempts remaining {countdown + 1}')
                    countdown -= 1
                password = input("Password: ")
            print("Banned from the system.")

    if flag:
        ans = input((f'Hotel with {email} email does not exist.\nCreate account? (y/n): '))
        if ans.lower() not in ('n', 'N'):
            sign_up()
        else:
            print('Goodbye!')


def sign_up():
    name = input('Name: \n')
    email = email_check()
    password = input('Password: \n')
    country=input('Country: \n')
    city=input('City: \n')
    av_rooms=int(input('Available rooms: \n'))
    pernightcost=float(input('Cost per night: \n'))
    

    customer = Hotel(name=name, email=email, password=password, country=country, city=city, available_rooms=av_rooms,pernightcost=pernightcost)
    ahotel.save()
    print('Account for {ahotel.name} hotel created successfully!')


def email_check():
    flag = 1
    email = input("Email: ")
    while True:
        flag = 0
        for smth in Hotel.objects.only('email'):
            if smth.email == email:
                email, flag = input(f"{email} already in use. Try a different one: "), 1
                break
        if not flag:
            break
    return email