import mongoengine as m
from bson.objectid import ObjectId
import datetime

bed_options=(1,2,3,4)
warning_options=(1,2,3,4,5)

class SpecialCustomer(m.EmbeddedDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	oid=m.ObjectIdField(required=True, default=lambda: ObjectId())
	customer=m.ObjectIdField(required=True)
	note=m.StringField()
	warning_level=m.IntField()