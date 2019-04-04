import mongoengine as m
from bson.objectid import ObjectId
import datetime
from Classes.admin_note import AdminNote

class AdminApplicant(m.EmbeddedDocument):
	registered_date=m.DateTimeField(default=datetime.datetime.now)
	oid=m.ObjectIdField(required=True, default=lambda: ObjectId())

	name=m.StringField(required=True)
	username=m.StringField(required=True,unique=True)
	gender=m.StringField(required=True)
	
	email=m.EmailField(required=True,unique=True)
	password=m.StringField(required=True)
	
	country=m.StringField(required=True)
	noteslist=m.EmbeddedDocumentListField(AdminNote)