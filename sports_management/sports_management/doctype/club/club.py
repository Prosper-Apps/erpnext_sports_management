# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Club(WebsiteGenerator):
	def get_context(self, context):

		# Set the page title
		context.page_title = self.name

		# Set the breadcrumbs
		context.parents = [{'name': 'Clubs', 'route': '/clubs'}]

		# Get the teams that are associated with the club and add it to the context
		context.teams = frappe.get_all("Team", filters={"club": self.name}, fields=["name", "route", "team_name", "sports_type"])

def get_list_context(context=None):

	context.update(
		{
			"title": "Clubs",
			"filters": {
				"owner": frappe.session.user
			}
		}		
	)

	# If the route is teams then get all the teams
	if frappe.local.request.path == "/clubs":
		del context.filters["owner"]