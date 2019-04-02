from mongoengine import QuerySet


class CustomerQuerySet(QuerySet):

	def best_paying(self):
		return self.filter(__raw__={'$where':'this.bookings.length>5'})

	def is_male(self):
		return self.filter(__raw__={'gender':'male'})

	def is_female(self):
		return self.filter(__raw__={'gender':'female'})

	def unknown_address(self):
		return self.filter(__raw__={'address':'Unknown'})