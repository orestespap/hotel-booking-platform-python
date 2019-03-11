from Classes.hotel import *
from Classes.customer import *
from Update_DB.update_db import *
import datetime
import numpy
import time

dashes='-'*5
def welcome_screen(ahotel):
	func_dict = {1:view_hotel_information,2:view_bookings,3:view_customers,4:revenue_stats,5:change_password,6:exit}
	#func_dict: dictionary containing function objects listed in the main menu

	check_low_av_rooms(ahotel)

	menu=f'{dashes}MENU{dashes}\n1.)View hotel information\n2.)View bookings\n3.)View customers\n4.)View revenue stats\n5.)Change password\n6.)Exit\nChoice: '

	print(f"Welcome {ahotel.name} :)")
	
	while True:
		ans=int(input(menu))
		while ans not in range(1,len(func_dict)+1):
			ans=int(input(f'Please type in a number from 1 to 5\n{menu}'))
		
		if ans==len(func_dict): func_dict[ans]() #exit()
		
		func_dict[ans](ahotel)

def change_password(ahotel):

	password=input('Please type in your current password: ')
	while password!=ahotel.password:
		password=input('Wrong password. Please try again: ')

	newpassword=input('Please type in your NEW password: ')
	while newpassword==password:
		newpassword=input('New password can\'t be the same with the current password.\nTry again: ')

	newpassword2=input('Retype your new password: ')
	while newpassword2!=newpassword:
		newpassword2=input('Passwords must match!\nTry again: ')

	update_db_change_user_password(ahotel,newpassword)
	print('Changes updated successfully.')

def view_hotel_information(ahotel):
	print(f'''--Hotel {ahotel.name} information--\n
	Location: {ahotel.address},{ahotel.city},{ahotel.country}\n
	Website: {ahotel.website}\n
	Stars: {ahotel.stars}/5\n
	Available rooms: {ahotel.available_rooms}\n
	Cost per night: {ahotel.pernightcost} Euro''')


def view_bookings(ahotel):
	while True:
		maintext='View today\'s bookings: (1)\nView all bookings: (2)\nBack to main menu: (3)\nChoice: '
		ans=int(input(maintext))
		while ans not in range(1,4):
			ans=int(input('Please select a number between 1 and 3.\n'+maintext))

		if ans is 1:
			count=0
			for abooking in ahotel.bookingslist:
				if str(abooking.registered_date).split()[0]==str(datetime.datetime.today()).split()[0]:
					reservation_info(abooking)
					count+=1
			if count:
				print(f'Great news! {count} reservation(s) today ({str(datetime.datetime.today()).split()[0]})!')
			else:
				print(f'Not any reservation\'s today; as of {str(datetime.datetime.today()).split()[-1]}')

		elif ans is 2:
			for abooking in ahotel.bookingslist:
				reservation_info(abooking)	
		else:
			break

def revenue_stats(ahotel):
	total_revenue,average_rpr=sum(abooking.cost for abooking in ahotel.bookingslist),numpy.mean(tuple(abooking.cost for abooking in ahotel.bookingslist))
	print(f'Your total revenue on the platform as of {str(datetime.datetime.today()).split()[0]} is {round(total_revenue,2)} Euro.\nYour average revenue per reservation is {round(average_rpr,2)} Euro.')
	time.sleep(5)

def reservation_info(abooking):
	customer=Customer.objects(id=abooking.customerid).first()
	print(f'''--RESERVATION INFORMATION--\n
							Customer name: {customer.name}\n
							Check in date: {abooking.check_in_date}\n
							Check out date: {abooking.check_out_date}\n
							Number of beds: {abooking.beds}\n
							Total cost of reservation: {abooking.cost} Euro\n
							Reservation date: {abooking.registered_date}''')

def check_low_av_rooms(ahotel):
	if ahotel.available_rooms<4:
		print(f'{dashes}WARNING{dashes}\nOnly {ahotel.available_rooms} room(s) are available for reservation.')
		time.sleep(3)
def view_customers(ahotel):
	#customerids=tuple(set(abooking.customerid for abooking in ahotel.bookingslist))
	customerids=tuple(abooking.customerid for abooking in ahotel.bookingslist)
	if not customerids:
		print("No customers yet!")
		return
	
	noofbookings={anid:customerids.count(anid) for anid in set(customerids)}

	for acustomerid in noofbookings:
		view_customer_info(acustomerid,noofbookings[acustomerid])

def view_customer_info(cid,bookings_count):
	acustomer=Customer.objects(id=cid).first()
	print(f'Name: {acustomer.name}\nUsername: {acustomer.username}\nEmail: {acustomer.email}\nCountry: {acustomer.email}\nAddress: {acustomer.address}\nNumber of bookings: {bookings_count}\n')