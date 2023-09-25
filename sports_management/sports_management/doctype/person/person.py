# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Person(WebsiteGenerator):
	def get_context(self, context):
		# Get the address doctype and add it to the context
		context.address = frappe.get_doc("Address", self.address)

		# Get the contact doctype and add it to the context
		context.contact = frappe.get_doc("Contact", self.contact)

		# Get a list of the teams that the person is a member of
		context.teams = frappe.get_all("Team Player", filters={"person": self.name}, fields=["parent"])

		# For each team get the team name and route
		for team in context.teams:
			team.route = frappe.get_value("Team", team.parent, "route")
