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
