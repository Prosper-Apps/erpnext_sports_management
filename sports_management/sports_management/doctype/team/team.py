# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Team(WebsiteGenerator):
	def get_context(self, context):

		tournaments = frappe.get_all('Tournament Team', 
			filters={'team': self.name}, fields=['parent', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'])
		
		# get the tournament teams along with the tournament name and route
		for tournament in tournaments:
			tournament.route = frappe.get_value('Tournament', tournament.parent, 'route')
			tournament.picture = frappe.get_value('Tournament', tournament.parent, 'picture')

		context.tournaments = tournaments
