import mongoengine as m
from bson.objectid import ObjectId
import datetime


class AdminNote(m.EmbeddedDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	oid=m.ObjectIdField(required=True, default=lambda: ObjectId())
	author_id=m.ObjectIdField(required=True) #admin user who wrote the note
	note=m.StringField(required=True)