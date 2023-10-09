# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Venue(WebsiteGenerator):
	def get_context(self, context):
		# Get the address doctype of the venue and add it to the context
		context.address = frappe.get_doc("Address", self.address)

		# Get the club associated with the venue and add it to the context
		context.club = frappe.get_doc("Club", self.club)

		# Get the teams that are associated with the club and add it to the context
		context.teams = frappe.get_all("Team", filters={"club": self.club}, fields=["name", "route"])

		# Get the matches that are associated with the venue and add it to the context
		context.matches = frappe.get_all("Match", filters={"venue": self.name}, fields=["name", "route", "home", "guest", "full_time_home_result", "full_time_guest_result", "date", "time", "venue"], order_by="date asc")

	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()
			