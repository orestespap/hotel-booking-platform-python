import mongoengine as m
import datetime
from Classes.special_hotel import SpecialHotel
from Classes.special_customer import SpecialCustomer
from Classes.adminapplicant import AdminApplicant

gender_options=['male','female','other']
gender_dict={'male':'Mr.','female':'Mrs.','other':'X.'}

class Admin(m.DynamicDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	
	name=m.StringField(required=True)
	username=m.StringField(required=True,unique=True)
	gender=m.StringField(required=True, choices=gender_options)
	
	email=m.EmailField(required=True,unique=True)
	password=m.StringField(required=True)
	
	country=m.StringField(required=True)
	
	
	hotelslist=m.EmbeddedDocumentListField(SpecialHotel)
	customerslist=m.EmbeddedDocumentListField(SpecialCustomer)
	applicationslist=m.EmbeddedDocumentListField(AdminApplicant)
	
	meta={
		'db_alias':'xyz',
		'collection':'administrators',
		'indexes':['username','email']
	}