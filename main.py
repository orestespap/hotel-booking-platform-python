import mongoengine as m
import datetime
from Homepage.access_type import select_account_type
#from Classes.customer import Customer
#from Classes.hotel import Hotel
#from Classes.admin import Admin
#from Tools.saveandgrab import jsonload_
#from mongoengine.queryset.visitor import Q

def set_up_mongo():
	m.register_connection(alias='xyz', name='hotels')

set_up_mongo()
select_account_type()

#must add close connection