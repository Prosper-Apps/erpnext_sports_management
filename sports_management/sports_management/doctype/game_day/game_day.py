# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.website.website_generator import WebsiteGenerator

class GameDay(WebsiteGenerator):
	def get_context(self, context):

		# Set the page title
		context.page_title = self.name

		# Set the breadcrumbs
		context.parents = [{"name": "Home", "route":"/"}, {"name": "Game Days", "route":"/game_days"}]

		# Get the tournament name and route
		context.tournament = frappe.get_doc("Tournament", self.tournament)

		# Get the matches with name and route
		context.matches = frappe.get_all('Match', filters={'game_day': self.name}, fields=['name', 'route', 'home', 'home_name', 'guest', 'guest_name', 'date', 'time', 'venue', 'full_time_home_result', 'full_time_guest_result', 'status'], order_by='date')
		for match in context.matches:
			match.time = (datetime.datetime.min + match.time).time().strftime('%H:%M')
