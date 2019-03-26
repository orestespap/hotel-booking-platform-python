import mongoengine as m
import datetime
from Classes.booking import Booking
from Custom_Query_Sets.customcustomersqs import CustomerQuerySet


gender_options=['male','female','other']
gender_dict={'male':'Mr.','female':'Mrs.','other':'X.'}
class Customer(m.DynamicDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	
	name=m.StringField(required=True)
	username=m.StringField(required=True,unique=True)
	gender=m.StringField(required=True, choices=gender_options)
	email=m.EmailField(required=True,unique=True)
	password=m.StringField(required=True)

	wallet=m.FloatField(default=0)
	country=m.StringField(default=None)
	city=m.StringField(default=None)
	address=m.StringField(default=None)


	bookings=m.EmbeddedDocumentListField(Booking)
	favoritehotels=m.ListField(m.ObjectIdField())


	meta={
		'db_alias':'xyz',
		'collection':'customers',
		'queryset_class': CustomerQuerySet
	}