# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Venue(WebsiteGenerator):
	def get_context(self, context):

		# Set the page title
		context.page_title = self.name

		# Set the breadcrumbs
		context.parents = [{'name': 'Home', 'route':'/'}, {'name': 'Venues', 'route':'/venues'}]

		# Get the matches that are associated with the venue and add it to the context
		context.matches = frappe.get_all("Match", filters={"venue": self.name}, fields=["name", "route", "tournament", "home", "home_name", "guest", "guest_name", "full_time_home_result", "full_time_guest_result", "date", "time", "status"], order_by="date asc")

	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()
			
def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": "Venues",
			"parents": [{"name": "Home", "route":"/"}],
			"filters": {
				"published": True
			}
		}
	)
