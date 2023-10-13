# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator

class SportsType(WebsiteGenerator):
	pass

def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": "Sports Types",
			"parents": [{"name": "Home", "route":"/"}],
		}
	)
