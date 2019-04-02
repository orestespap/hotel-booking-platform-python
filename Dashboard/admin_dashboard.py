from Classes.hotel import *
from Classes.customer import *
from Classes.booking import *
from Classes.special_hotel import *
from Update_DB.update_db import *
from mongoengine.queryset.visitor import Q


def welcome_screen(anadmin):
	func_dict = {1:view_hotels,2:edit_shady_hotels,3:edit_shady_customers,4:None,5:None,6:filter_hotels,7:filter_customers,8:change_password,9:manage_applications,10:exit}
	#4:delete_hotel_sys,5:delete_customer_sys}
	
	#func_dict: dictionary containing function objects listed in the main menu

	#delete hotel and customer functions should be implemented in the update_db file
	#Upcoming feature: Platform admin applications; create relevant embedded document

	dashes='-'*5
	menu=f'{dashes}MAIN MENU{dashes}\n1.)View hotels\n2.)Edit shady hotels\n3.)Edit shady customers\n4.)Delete hotel from system\n5.)Delete customer\n6.)Filter hotels\n7.)Filter customers\n8.)Change your password\n9.)Edit admin applications\n10.)Exit\nChoice: '

	print(f"Welcome {anadmin.name} :)")
	
	while True:
		ans=int(input(menu))
		while ans not in range(1,len(func_dict)+1):
			ans=int(input(f'Please type in a number from 1 to 5\n{menu}'))
		
		if ans==len(func_dict): func_dict[ans]() #exit()
		
		func_dict[ans](anadmin)

def view_hotels(anadmin=None):
	for index,ahotel in enumerate(Hotel.objects.only('name')):
		print(f'{index+1}.) {ahotel.name}')
	#Need to insert view hotel information function and a functional selection menu

def view_customers(anadmin=None):
	for index,acustomer in enumerate(Customer.objects.only('username')):
		print(f'{index+1}.) {acustomer.username}')

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



def filter_customers(anadmin):
	dashes='-'*5
	
	specialtext={1:f"{dashes}BEST PAYING USERS{dashes}",2:f'{dashes}MALE USERS{dashes}',3:f'{dashes}FEMALE USERS{dashes}',4:f'{dashes}USERS WITH UNKNOWN ADDRESS{dashes}'}
	func_dict={1:Customer.objects.best_paying,2:Customer.objects.is_male,3:Customer.objects.is_female,4:Customer.objects.unknown_address}
	
	menu=f'{dashes}HOTEL FILTERS MENU{dashes}\n1.)View best paying users\n2.)View male users\n3.)View female users\n4.)View users without address\n5.)Return to main menu'
	
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
		users=func_dict[ans]()
		
		if not users:
			print("None.")
		else:	
			for auser in users:
				view_user_information(auser)


#SHADY HOTELS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def view_shady_hotels(anadmin):
	for index,ashadyhotel in enumerate(anadmin.hotelslist):
		print(f'{index+1}.) {Hotel.objects(id=ashadyhotel.hotel).first().name}')


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

def edit_shady_hotels(anadmin):
	func_dict = {1:view_shady_hotels,2:add_shady_hotel,3:remove_shady_hotels,4:edit_note,5:edit_warning_level}
	dashes='-'*5
	menu=f'{dashes}SHADY HOTELS MENU{dashes}\n1.)View shady hotel information\n2.)Add shady hotel to list\n3.)Remove hotel from list\n4.)Edit note\n5.)Edit warning level\n6.)Return to main menu\nChoice: '
	
	while True:
		while True:
			ans=int(input(menu+'\nChoice: '))
			if ans not in range(1,len(func_dict)+2):
				ans=int(input(f'Please type in a number from 1 to 6\n{menu}!'))
			else:
				if ans==len(func_dict)+1:
					return
				break
		if ans==4 or ans==5:
			func_dict[ans](anadmin,'h')
		else:	
			func_dict[ans](anadmin)


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


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#SHADY USERS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def edit_shady_customers(anadmin):
	
	func_dict = {1:view_shady_customers,2:add_shady_user,3:remove_shady_users,4:edit_note,5:edit_warning_level}
	dashes='-'*5
	menu=f'{dashes}SHADY CUSTOMERS MENU{dashes}\n1.)View shady customers\' information\n2.)Add shady customer to list\n3.)Remove customer from list\n4.)Edit note\n5.)Edit warning level\n6.)Return to main menu\nChoice: '
	
	while True:
		while True:
			ans=int(input(menu+'\nChoice: '))
			if ans not in range(1,len(func_dict)+2):
				ans=int(input(f'Please type in a number from 1 to 6\n{menu}!'))
			else:
				if ans==len(func_dict)+1:
					return
				break
		if ans==4 or ans==5:
			func_dict[ans](anadmin,'c')
		else:
			func_dict[ans](anadmin)


def view_shady_customers(anadmin):
	if not anadmin.customerslist:
		print('List empty.')
		return
	
	for index,acustomer in enumerate(anadmin.customerslist):
		print(f'{index+1}.) @{Customer.objects(id=acustomer.customerid).first().username}')


def add_shady_user(anadmin):
	#add return to sahdy menu option
	while True:
		while True:
			view_customers()
			ans=int(input('Select a user:\n'))
			if ans in range(1,len(Customer.objects)+1):
				break
			print(f'Please type in an integere from 1 to {len(Customer.objects)}')

		acustomer=tuple(acustomer for index,acustomer in enumerate(Customer.objects) if index+1==ans)[0]
		
		if not Admin.objects(Q(id=anadmin.id) & Q(customerslist__customerid=acustomer.id)):
			specialcustomer=SpecialCustomer(customerid=acustomer.id)
			update_db_add_shady_customer(anadmin,specialcustomer)
			print(f'User @{acustomer.username} added to list of shady customers successfully!')
			break
		print(f'User @{acustomer.username} is already in your list of shady customers.')


def remove_shady_users(anadmin):
	if not anadmin.customerslist:
		print('List empty.')
		return
	while True:
		while True:
			view_shady_customers(anadmin)
			print(f'{len(anadmin.customerslist)+1}.) Back to main menu')

			ans=int(input('Select user: '))
			
			if ans in range(1,len(anadmin.customerslist)+2):
				if ans==len(anadmin.customerslist)+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
	
		acustomer=tuple(acustomer for index,acustomer in enumerate(anadmin.customerslist) if index+1==ans)[0]
		update_db_remove_shady_customer(anadmin,acustomer)
		print(f'@{Customer.objects(id=acustomer.customerid).first().username} successfully removed from shady customers list!')


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Edit note and warning level functions, abstracted in order cover both both special_hotel and special_customer



def edit_note(anadmin,key):
	option={'c':{'admin_struct':anadmin.customerslist},'h':{'admin_struct':anadmin.hotelslist}}

	shadyobject=option[key]
	while True:
		while True:
			view_shady_objects(anadmin,key)
			print(f'{len(shadyobject["admin_struct"])+1}.)Back to main menu')

			ans=int(input('Choice: '))
			
			if ans in range(1,len(shadyobject['admin_struct'])+2):
				if ans==len(shadyobject['admin_struct'])+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
		
		ashadyobject=tuple(ashadyobject for index,ashadyobject in enumerate(shadyobject['admin_struct']) if index+1==ans)[0]
		print(f'Current note\n{ashadyobject.note}')
		ans=input('Please type in new note:\n')
		
		while not ans:
			ans=input('Note cannot be empyt: \n')
			if ans: break
		
		update_db_edit_note(anadmin,ashadyobject,ans,key)
		print_success(ashadyobject,key,'note')

def edit_warning_level(anadmin,key):
	option={'c':{'admin_struct':anadmin.customerslist},'h':{'admin_struct':anadmin.hotelslist}}

	shadyobject=option[key]

	while True:
		while True:
			view_shady_objects(anadmin,key)
			print(f'{len(shadyobject["admin_struct"])+1}.)Back to main menu')

			ans=int(input('Choice: '))
			
			if ans in range(1,len(shadyobject['admin_struct'])+2):
				if ans==len(shadyobject['admin_struct'])+1:
					return
				break
			print(f'Please type in an integere from 1 to {index+1}')
		ashadyobject=tuple(ashadyobject for index,ashadyobject in enumerate(shadyobject['admin_struct']) if index+1==ans)[0]
		print(f'Current warning level: {ashadyobject.warning_level}')
		ans=int(input(f'New warning level ({warning_options[0]}-{warning_options[-1]}):\n'))
		
		while ans not in warning_options:
			ans=input(f'Warning level must be an integer from {warning_options[0]} to {warning_options[-1]}: \n')
			if ans: break
		
		update_db_edit_warning_level(anadmin,ashadyobject,ans,key)
		print_success(ashadyobject,key,'wl')

def print_success(ashadyobject,key,from_):
	if from_=='wl':
		if key=='h':
			print(f'{Hotel.objects(id=ashadyobject.hotel).first().name} hotel\'s warning level edited successfully!')
		else:
			print(f'{Customer.objects(id=ashadyobject.customerid).first().name} user\'s warning level edited successfully!')
	else:
		if key=='h':
			print(f'Note for {Hotel.objects(id=ashadyobject.hotel).first().name} edited successfully!')
		else:
			print(f'Note for {Customer.objects(id=ashadyobject.customerid).first().name} edited successfully!')



def view_shady_objects(anadmin,key):
	if key=='h':
		view_shady_hotels(anadmin)
	else:
		view_shady_customers(anadmin)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#applications manager
def manage_applications(anadmin):
	func_dict,dashes= {1:view_applications,2:edit_applications_main},'-'*5
	menu=f'{dashes}ADMIN APPLICATIONS MENU{dashes}\n1.)View applications\n2.)Edit applications\n3.)Return to main menu'
	
	check_for_new_applications(anadmin)
	while True:
		while True:
			ans=int(input(menu+'\nChoice: '))
			if ans not in range(1,len(func_dict)+2):
				ans=int(input(f'Please type in a number from 1 to {len(func_dict)+1}\n{menu}'))
			else:
				if ans==len(func_dict)+1:
					return
				break 
		users=func_dict[ans](anadmin)

def view_applications(anadmin):
	for an_applicant in anadmin.applicationslist:
		print(f'Name: {an_applicant.name}\nGender: {an_applicant.gender}\nEmail: {an_applicant.email}\nCountry: {an_applicant.country}\nRequested username: {an_applicant.username}\nSubmission id: {an_applicant.oid}\nSubmission date: {an_applicant.registered_date}\n')

def view_application(an_applicant):
	print(f'Name: {an_applicant.name}\nGender: {an_applicant.gender}\nEmail: {an_applicant.email}\nCountry: {an_applicant.country}\nRequested username: {an_applicant.username}\nSubmission id: {an_applicant.oid}\nSubmission date: {an_applicant.registered_date}\n')
	#Note: {an_applicant.note}\n

def view_applications_as_list(anadmin):
	for index,an_applicant in enumerate(anadmin.applicationslist):
		print(f'{index+1}.)Email: {an_applicant.email}, ID: {an_applicant.oid}')
	print(f'{len(anadmin.applicationslist)+1}.)Cancel\n')

def edit_applications_main(anadmin):
	
	while True:
		view_applications_as_list(anadmin)
		ans=int(input('Choice: '))
		if ans not in range(1,len(anadmin.applicationslist)+2):
			print(f'Please type in an integere from 1 to {anadmin.applicationslist+1}')
		if ans==len(anadmin.applicationslist)+1:
			return
		else:
			edit_application(anadmin,anadmin.applicationslist[ans-1],ans-1)

def edit_application(anadmin,an_applicant,pos):
	func_dict={1:update_db_accept_application,2:update_db_reject_application,3:edit_note}
	view_application(an_applicant)

	while True:
		ans=int(input('1.)Accept application\n2.)Reject application\n3.)Edit note\n4.)Cancel\nChoice: '))
		if ans not in range(1,len(func_dict)+2):
			print(f'Please type in an integere from 1-{len(func_dict)+2}')
		elif ans==len(func_dict)+1:
			return
		elif ans==len(func_dict):
			func_dict[ans](anadmin.id,an_applicant) #pos
		else:
			break
	func_dict[ans](an_applicant)

def edit_note(adminid,an_applicant):
	#just new note for now
	#need to add view and edit notes written by admin

	anote=input('New note:')
	update_db_add_application_note(anote,adminid,an_applicant)

def check_for_new_applications(anadmin):
	noofnewappl=tuple(an_applicant.oid for an_applicant in anadmin.applicationslist if str(an_applicant.registered_date).split()[0]==str(datetime.datetime.today()).split()[0])
	if noofnewappl:
		print(f'---NOTIFICATION---\n{len(noofnewappl)} new admin application(s) submitted today!')
	
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
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

def view_user_information(auser):
	print(f'''--{auser.name} information--\n
	Username: {auser.username}\n
	Email: {auser.email}\n
	Location: {auser.address},{auser.city},{auser.country}\n
	Gender: {auser.gender}\n
	No of bookings: {len(auser.bookings)}\n''')