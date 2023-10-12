# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Team(WebsiteGenerator):
	def get_context(self, context):

		# Define the title of the page
		context.title = self.team_name

		# Define breadcrumbs
		context.parents = [{"name": "Home", "route":"/"}, {"name": "Teams", "route":"/teams"}]

		tournaments = frappe.get_all('Ranking', 
			filters={'team': self.name}, fields=['tournament', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'])
		
		# get the tournament teams along with the tournament name and route
		for tournament in tournaments:
			tournament.route = frappe.get_value('Tournament', tournament.tournament, 'route')
			tournament.picture = frappe.get_value('Tournament', tournament.tournament, 'picture')
			tournament.tournament_name = frappe.get_value('Tournament', tournament.tournament, 'tournament_name')

		context.tournaments = tournaments

		# Get the club doctype of the team and add it to the context
		context.club = frappe.get_doc("Club", self.club)

		# Get the matches that are associated with the club and add it to the context
		context.matches = frappe.get_all("Match", filters={"home": self.name}, fields=["name", "route", "home", "home_name", "guest", "guest_name", "full_time_home_result", "full_time_guest_result", "date", "time", "venue", "status"], order_by="date asc")	
		context.matches += frappe.get_all("Match", filters={"guest": self.name}, fields=["name", "route", "home", "home_name", "guest", "guest_name", "full_time_home_result", "full_time_guest_result", "date", "time", "venue", "status"], order_by="date asc")	
		# Order the context.matches by date
		context.matches = sorted(context.matches, key=lambda k: k['date'])	

	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()
			