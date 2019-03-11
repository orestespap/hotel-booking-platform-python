from mongoengine import QuerySet


class HotelQuerySet(QuerySet):

	def is_five_star(self):
		return self.filter(stars=5)

	def premium_hotels(self):
		return self.filter(pernightcost__gt=500)

	def overbooked(self):
		return self.filter(__raw__={"$where":"this.bookingslist.length > 10"})

	def fully_booked(self):
		return self.filter(__raw__={"available_rooms":0})