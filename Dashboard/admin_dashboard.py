from Classes.hotel import *
from Classes.customer import *
from Classes.booking import *
from Classes.special_hotel import *
from Update_DB.update_db import *
from mongoengine.queryset.visitor import Q


def welcome_screen(anadmin):
	func_dict = {1:view_hotels,2:view_shady_users,3:edit_shady_hotels,4:None,5:None,6:None,7:filter_hotels,8:change_password,9:exit}
	#4:edit_shady_customers,5:delete_hotel_sys,6:delete_customer_sys}
	
	#func_dict: dictionary containing function objects listed in the main menu

	#delete hotel and customer functions should be implemented in the update_db file

	dashes='-'*5
	menu=f'{dashes}MAIN MENU{dashes}\n1.)View hotels\n2.)View shady users\n3.)Edit shady hotels\n4.)Edit shady customers\n5.)Delete hotel from system\n6.)Delete customer\n7.)Filter hotels\n8.)Change your password\n9.)Exit\nChoice: '

	print(f"Welcome {anadmin.name} :)")
	
	while True:
		ans=int(input(menu))
		while ans not in range(1,len(func_dict)+1):
			ans=int(input(f'Please type in a number from 1 to 5\n{menu}'))
		
		#if ans==len(func_dict): func_dict[ans]() #exit()
		
		func_dict[ans](anadmin)

def view_hotels(anadmin=None):
	for index,ahotel in enumerate(Hotel.objects.only('name')):
		print(f'{index+1}.) {ahotel.name}')
	#Need to insert view hotel information function and a functional selection menu

def view_shady_users(anadmin):
	for index,acustomer in enumerate(anadmin.customerslist):
		print(f'{index+1}.) {Customer.objects(id=acustomer.customer).first().name}')
	#Need to create and insert view customer information function and a functional selection menu

def filter_hotels(anadmin):
	dashes='-'*5
	
	specialtext={1:f"{dashes}5 STAR HOTELS{dashes}",2:f'{dashes}PREMIUM HOTELS{dashes}',3:f'{dashes}OVERBOOKED HOTELS{dashes}',4:f'{dashes}FULLY BOOKED HOTELS{dashes}'}
	func_dict={1:Hotel.objects.is_five_star,2:Hotel.objects.premium_hotels,3:Hotel.objects.overbooked,4:Hotel.objects.fully_booked}
	
	menu=f'{dashes}HOTEL FILTERS MENU{dashes}\n1.)View 5 star hotels\n2.)View premium hotels\n3.)View overbooked hotels\n4.)View fully booked hotels\n5.)Return to main menu'
	
	while True:
		while True:
			ans=int(input(menu+'\nChoice: '))
			if ans not in range(1,len(specialtext)+2):
				ans=int(input(f'Please type in a number from 1 to {len(specialtext)+1}\n{menu}'))
			else:
				if ans==len(specialtext)+1:
					return
				break 
		print(specialtext[ans])
		hotels=func_dict[ans]()
		
		if not hotels:
			print("None.")
		else:	
			for ahotel in hotels:
				view_hotel_information(ahotel)


def edit_shady_hotels(anadmin):
	func_dict = {1:view_shady_hotels,2:add_shady_hotel,3:remove_shady_hotels,4:edit_note,5:edit_warning_level}
	dashes='-'*5
	menu=f'{dashes}SHADY HOTELS MENU{dashes}\n1.)View shady hotel information\n2.)Add shady hotel to list\n3.)Remove hotel from list\n4.)Edit note\n5.)Edit warning level\n6.)Return to main menu\nChoice: '
	
	while True:
		while True:
			ans=int(input(menu+'\nChoice: '))
			if ans not in range(1,len(func_dict)+2):
				ans=int(input(f'Please type in a number from 1 to 6\n{menu}'))
			else:
				if ans==len(func_dict)+1:
					return
				break
		func_dict[ans](anadmin)

def view_shady_hotels(anadmin):
	for index,ashadyhotel in enumerate(anadmin.hotelslist):
		print(f'{index+1}.) {Hotel.objects(id=ashadyhotel.hotel).first().name}')

def edit_note(anadmin):
	while True:
		while True:
			view_shady_hotels(anadmin)
			print(f'{len(anadmin.hotelslist)+1}.)Back to main menu')

			ans=int(input('Choice: '))
			
			if ans in range(1,len(anadmin.hotelslist)+2):
				if ans==len(anadmin.hotelslist)+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
		ahotel=tuple(ahotel for index,ahotel in enumerate(anadmin.hotelslist) if index+1==ans)[0]
		print(f'Current note\n{ahotel.note}')
		ans=input('Please type in new note:\n')
		
		while not ans:
			ans=input('Note cannot be empyt: \n')
			if ans: break
		
		update_db_edit_note(anadmin,ahotel,ans)
		print(f'Note for {Hotel.objects(id=ahotel.hotel).first().name} edited successfully!')

def edit_warning_level(anadmin):
	while True:
		while True:
			view_shady_hotels(anadmin)
			print(f'{len(anadmin.hotelslist)+1}.)Back to main menu')

			ans=int(input('Choice: '))
			
			if ans in range(1,len(anadmin.hotelslist)+2):
				if ans==len(anadmin.hotelslist)+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
		ahotel=tuple(ahotel for index,ahotel in enumerate(anadmin.hotelslist) if index+1==ans)[0]
		print(f'Current warning level: {ahotel.warning_level}')
		ans=int(input(f'New warning level ({warning_options[0]}-{warning_options[-1]}):\n'))
		
		while ans not in warning_options:
			ans=input(f'Warning level must be an integer from {warning_options[0]} to {warning_options[-1]}: \n')
			if ans: break
		
		update_db_edit_warning_level(anadmin,ahotel,ans)
		print(f'{Hotel.objects(id=ahotel.hotel).first().name} hotel\'s warning level edited successfully!')


def add_shady_hotel(anadmin):
	#add return to sahdy menu option
	while True:
		while True:
			view_hotels()
			ans=int(input('Select a hotel:\n'))
			if ans in range(1,len(Hotel.objects)+1):
				break
			print(f'Please type in an integere from 1 to {len(Hotel.objects)}')

		ahotel=tuple(ahotel for index,ahotel in enumerate(Hotel.objects) if index+1==ans)[0]
		
		if not Admin.objects(Q(id=anadmin.id) & Q(hotelslist__hotel=ahotel.id)):
			specialhotel=SpecialHotel(hotel=ahotel.id)
			update_db_add_shady_hotel(anadmin,specialhotel)
			print(f'{ahotel.name} hotel added to list of shady hotels successfully!')
			break
		print(f'{ahotel.name} hotel is already in your list of shady hotels.')


def remove_shady_hotels(anadmin):
	while True:
		while True:
			view_shady_hotels(anadmin)
			print(f'{len(anadmin.hotelslist)+1}.) Back to main menu')

			ans=int(input('Select hotel: '))
			
			if ans in range(1,len(anadmin.hotelslist)+2):
				if ans==len(anadmin.hotelslist)+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
	
		ahotel=tuple(ahotel for index,ahotel in enumerate(anadmin.hotelslist) if index+1==ans)[0]
		update_db_remove_shady_hotel(anadmin,ahotel)
		print(f'{Hotel.objects(id=ahotel.hotel).first().name} successfully removed from shady hotels list!')


def change_password(anadmin):
	password=input('Please type in your current password: ')
	while password!=anadmin.password:
		password=input('Wrong password. Please try again: ')

	newpassword=input('Please type in your NEW password: ')
	while newpassword==password:
		newpassword=input('New password can\'t be the same with the current password.\nTry again: ')

	newpassword2=input('Retype your new password: ')
	while newpassword2!=newpassword:
		newpassword2=input('Passwords must match!\nTry again: ')

	update_db_change_admin_password(anadmin,newpassword)
	print('Changes updated successfully.')


def view_hotel_information(ahotel):
	print(f'''--{ahotel.name} hotel information--\n
	Location: {ahotel.address},{ahotel.city},{ahotel.country}\n
	Website: {ahotel.website}\n
	Stars: {ahotel.stars}/5\n
	Available rooms: {ahotel.available_rooms}\n
	Cost per night: {ahotel.pernightcost}''')