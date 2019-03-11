from Classes.hotel import *
from Classes.customer import *
from Classes.booking import *
from Update_DB.update_db import *


def welcome_screen(acustomer):
	func_dict = {1: view_hotels,2:book_a_room,3:view_bookings,4:change_password,5:exit}
	#func_dict: dictionary containing function objects listed in the main menu

	dashes='-'*5
	menu=f'{dashes}MENU{dashes}\n1.)View hotel information\n2.)Book a room\n3.)View bookings\n4.)Change your password\n5.)Exit\nChoice: '

	print(f"Welcome {acustomer.name} :)")
	
	while True:
		ans=int(input(menu))
		while ans not in range(1,len(func_dict)+1):
			ans=int(input(f'Please type in a number from 1 to 5\n{menu}'))
		
		if ans==len(func_dict): func_dict[ans]() #exit()
		
		func_dict[ans](acustomer)

def view_hotels(acustomer=None):
	for index,ahotel in enumerate(Hotel.objects.only('name')):
		print(f'{index+1}.) {ahotel.name}')
	#Need to insert view hotel information function and a functional selection menu

def change_password(acustomer):

	password=input('Please type in your current password: ')
	while password!=acustomer.password:
		password=input('Wrong password. Please try again: ')

	newpassword=input('Please type in your NEW password: ')
	while newpassword==password:
		newpassword=input('New password can\'t be the same with the current password.\nTry again: ')

	newpassword2=input('Retype your new password: ')
	while newpassword2!=newpassword:
		newpassword2=input('Passwords must match!\nTry again: ')

	update_db_change_user_password(acustomer,newpassword)
	print('Changes updated successfully.')

def view_hotel_information(ahotel):
	print(f'''--Hotel {ahotel.name} information--\n
	Location: {ahotel.address},{ahotel.city},{ahotel.country}\n
	Website: {ahotel.website}\n
	Stars: {ahotel.stars}/5\n
	Available rooms: {ahotel.available_rooms}\n
	Cost per night: {ahotel.pernightcost}''')


def view_bookings(acustomer):
	for abooking in acustomer.bookings:
		print(f'''--RESERVATION INFORMATION--\n
					Hotel: {abooking.hotel}\n
					Check in date: {abooking.check_in_date}\n
					Check out date: {abooking.check_out_date}\n
					Number of beds: {abooking.beds}\n
					Total cost of reservation: {abooking.cost}\n
					Reservation date: {abooking.registered_date}''')


def book_a_room(acustomer):
	num_hotels= Hotel.objects.count()
	print(f'Select a hotel!')
	hotels_dict={index+1:ahotel for index,ahotel in enumerate(Hotel.objects)}

	while True:
		while True:
			view_hotels()
			ans=int(input(f'---\n{num_hotels+1}.) Back to main menu\nSelect a number between 1 and {num_hotels+1}: '))
			while ans not in range(1,num_hotels+2):
				ans=input(f'Please select a number from 1 to {num_hotels+1}: ')
		
			if ans is num_hotels+1:
				return
			
			selected_hotel=hotels_dict[ans]
			if selected_hotel.available_rooms is 0:
				print(f'{selected_hotel.name} has no available rooms. Please choose another hotel.')
			else:
				break

		view_hotel_information(selected_hotel)
		while True:
			check_in_date,check_out_date=input("Check in date (MM/DD): ")+'/2019',input("Check out date (MM/DD): ")+'/2019'
			nights=int(check_out_date.split('/')[1])-int(check_in_date.split('/')[1])
			booking_cost=nights*selected_hotel.pernightcost

			if booking_cost<=acustomer.wallet:
				break
			print(f'''\nYour current balance is: {acustomer.wallet} Euro. The total fee of your booking is {booking_cost}Euro''')

		beds=int(input(f"How many beds? 1-{len(bed_options)}"))
		while beds not in range(1,len(bed_options)+1):
			beds=int(input(f"Number of beds must be 1-{len(bed_options)}: "))

		abooking=Booking(customerid=acustomer.id,hotel=selected_hotel.name,beds=beds,cost=booking_cost,check_in_date=check_in_date,check_out_date=check_out_date)
		update_db_complete_booking(acustomer,abooking,selected_hotel)
		booking_completed(acustomer,abooking)


def booking_completed(acustomer,abooking):
	surname=acustomer.name.split(' ')[-1]
	print(f'Dear {gender_dict[acustomer.gender]} {surname},\nYour reservation at the {abooking.hotel} hotel from {abooking.check_in_date} to {abooking.check_out_date} has been booked successfully.')