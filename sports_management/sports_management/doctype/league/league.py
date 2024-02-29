# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class League(WebsiteGenerator):
	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()

	def get_context(self, context):
		
		# Define the title of the page
		context.title = self.league_name

		# Define breadcrumbs
		context.parents = [{"name": "Home", "route":"/"}, {"name": "Leagues", "route":"/leagues"}]

		# Get the tournaments with name and route
		context.tournaments = frappe.get_all('Tournament', filters={'league': self.name, "published": True}, fields=['name', 'route', 'tournament_name', 'picture'], order_by='ordering asc')

def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": "Leagues",
			"parents": [{"name": "Home", "route":"/"}],
			"filters": {
				"published": True
			},
			"order_by": "ordering asc"
		}
	)
