import mongoengine as m
import datetime
from Classes.booking import Booking
from Custom_Query_Sets.customhotelqs import HotelQuerySet


star_options=[1,2,3,4,5]
class Hotel(m.DynamicDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	
	name=m.StringField(required=True)
	email=m.EmailField(required=True,unique=True)
	password=m.StringField(required=True)

	country=m.StringField(required=True)
	city=m.StringField(required=True)
	address=m.StringField(default=None)
	website=m.URLField(default=None)

	available_rooms=m.IntField(required=True)
	pernightcost=m.FloatField(required=True)
	stars=m.IntField(choices=star_options)

	bookingslist=m.EmbeddedDocumentListField(Booking)

	meta={
		'db_alias':'xyz',
		'collection':'hotels',
		'queryset_class': HotelQuerySet
	}