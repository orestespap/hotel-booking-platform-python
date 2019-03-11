import mongoengine as m
from bson.objectid import ObjectId
import datetime

bed_options=[1,2,3,4]


class Booking(m.EmbeddedDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	oid=m.ObjectIdField(required=True, default=lambda: ObjectId())
	beds=m.IntField(required=True, choices=bed_options)
	hotel=m.StringField(required=True)

	customerid=m.ObjectIdField()
	check_in_date=m.DateTimeField(required=True)
	check_out_date=m.DateTimeField(required=True)

	cost=m.FloatField()