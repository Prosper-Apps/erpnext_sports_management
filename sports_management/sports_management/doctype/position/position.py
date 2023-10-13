# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator

class Position(WebsiteGenerator):
	def get_context(self, context):

		# Insert page title
		context.page_title = self.name

		# Add bredcrumb
		context.parents = [{'name': 'Positions', 'route': '/positions'}]

def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": "Positions",
			"parents": [{"name": "Home", "route":"/"}],
		}
	)
