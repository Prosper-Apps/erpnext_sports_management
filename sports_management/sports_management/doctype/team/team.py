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

		# Get the club doctype of the team and add it to the context
		context.club = frappe.get_doc("Club", self.club)

		# Get the venue doctype and add it to the context if it exists
		if self.venue:
			context.venue = frappe.get_doc("Venue", self.venue)

		# For each of the team_player get the name and route and add it to the context
		for team_player in context.team_player:
			team_player.route = frappe.get_value('Person', team_player.person, 'route')
			team_player.name = frappe.get_value('Person', team_player.person, 'name')
			team_player.picture = frappe.get_value('Person', team_player.person, 'picture')

		# Do the same for the team staff
		for team_staff in context.team_staff:
			team_staff.route = frappe.get_value('Person', team_staff.person, 'route')
			team_staff.name = frappe.get_value('Person', team_staff.person, 'name')
			team_staff.picture = frappe.get_value('Person', team_staff.person, 'picture')

		# The same for the team coach
		for team_coach in context.team_coach:
			team_coach.route = frappe.get_value('Person', team_coach.person, 'route')
			team_coach.name = frappe.get_value('Person', team_coach.person, 'name')
			team_coach.picture = frappe.get_value('Person', team_coach.person, 'picture')

		# Get the matches that are associated with the club and add it to the context
		context.matches = frappe.get_all("Match", filters={"home": self.name}, fields=["name", "route", "home", "guest", "full_time_home_result", "full_time_guest_result", "date", "time", "venue"], order_by="date asc")	
		context.matches += frappe.get_all("Match", filters={"guest": self.name}, fields=["name", "route", "home", "guest", "full_time_home_result", "full_time_guest_result", "date", "time", "venue"], order_by="date asc")	
		# Order the context.matches by date
		context.matches = sorted(context.matches, key=lambda k: k['date'])	
