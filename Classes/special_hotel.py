import mongoengine as m
from bson.objectid import ObjectId
import datetime


warning_options=(0,1,2,3,4,5)

class SpecialHotel(m.EmbeddedDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	oid=m.ObjectIdField(default=lambda: ObjectId())
	hotel=m.ObjectIdField(required=True)
	note=m.StringField(default="N/A")
	warning_level=m.IntField(default=0)