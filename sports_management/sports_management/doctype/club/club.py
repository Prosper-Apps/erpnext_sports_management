# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Club(WebsiteGenerator):
	def get_context(self, context):
		# Get the address doctype of the venue and add it to the context
		context.address = frappe.get_doc("Address", self.address)

		# Get the contact doctype of the venue and add it to the context
		context.contact = frappe.get_doc("Contact", self.contact)

		# Get the venue doctype and add it to the context
		context.venue = frappe.get_doc("Venue", self.venue)


