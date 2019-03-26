from Classes.hotel import *
from Classes.customer import *
from Classes.booking import *
from Classes.admin import *


def update_db_complete_booking(acustomer,abooking,ahotel):
	Customer.objects(id=acustomer.id).update_one(push__bookings=abooking)
	Customer.objects(id=acustomer.id).update_one(dec__wallet=abooking.cost)
	acustomer.reload()

	Hotel.objects(id=ahotel.id).update_one(push__bookingslist=abooking)
	Hotel.objects(id=ahotel.id).update_one(dec__available_rooms=1)
	ahotel.reload()

def update_db_change_user_password(acustomer,newpassword):
	Customer.objects(id=acustomer.id).update_one(__raw__={"$set":{"password":newpassword}})
	acustomer.reload()

def update_db_change_hotel_password(ahotel,newpassword):
	Hotel.objects(id=ahotel.id).update_one(__raw__={"$set":{"password":newpassword}})
	ahotel.reload()

def update_db_change_admin_password(anadmin,newpassword):
	Admin.objects(id=anadmin.id).update_one(__raw__={"$set":{"password":newpassword}})
	anadmin.reload()

def update_db_add_shady_hotel(anadmin,aspecialhotel):
	Admin.objects(id=anadmin.id).update_one(push__hotelslist=aspecialhotel)
	anadmin.reload()

def update_db_remove_shady_hotel(anadmin,aspecialhotel):
	Admin.objects(id=anadmin.id).update_one(pull__hotelslist=aspecialhotel)
	anadmin.reload()


def update_db_add_shady_customer(anadmin,aspecialcustomer):
	Admin.objects(id=anadmin.id).update_one(push__customerslist=aspecialcustomer)
	anadmin.reload()

def update_db_remove_shady_customer(anadmin,aspecialcustomer):
	Admin.objects(id=anadmin.id).update_one(pull__customerslist=aspecialcustomer)
	anadmin.reload()

def update_db_edit_note(anadmin,ashadyobject,new_note,key):
	if key=='h':
		for index,ahotel in enumerate(anadmin.hotelslist):
			if ahotel.oid==ashadyobject.oid:
				anadmin.hotelslist[index].note=new_note
	else:
		for index,acustomer in enumerate(anadmin.customerslist):
			if acustomer.oid==ashadyobject.oid:
				anadmin.customerslist[index].note=new_note

	anadmin.save()
	anadmin.reload()

def update_db_edit_warning_level(anadmin,ashadyobject,new_wl,key):
	if key=='h':
		for index,ahotel in enumerate(anadmin.hotelslist):
			if ahotel.oid==ashadyobject.oid:
				anadmin.hotelslist[index].warning_level=new_wl
	else:
		for index,acustomer in enumerate(anadmin.customerslist):
			if acustomer.oid==ashadyobject.oid:
				anadmin.customerslist[index].warning_level=new_wl

	anadmin.save()
	anadmin.reload()