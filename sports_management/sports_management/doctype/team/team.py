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

		# Get the rankings that are associated with the team and add it to the context
		tournaments = frappe.get_all('Ranking', 
			filters={"team": self.name}, fields=['tournament', 'tournament.published', 'rank', 'played', 'wins', 'draws', 'losses', 'points', 'score_for', 'score_against', 'difference'])
		
		# Remove the rankings that are associated with tournaments that are not published
		tournaments = [tournament for tournament in tournaments if tournament.published == 1]
		
		# get the tournament teams along with the tournament name and route
		for tournament in tournaments:
			tournament.route = frappe.get_value('Tournament', tournament.tournament, 'route')
			tournament.picture = frappe.get_value('Tournament', tournament.tournament, 'picture')
			tournament.tournament_name = frappe.get_value('Tournament', tournament.tournament, 'tournament_name')
			# Get the matches that are associated with the team and add it to the context
			tournament.matches = frappe.get_all("Match", filters={"home": self.name, "tournament": tournament.tournament}, fields=["name", "route", "home", "home_name", "guest", "guest_name", "full_time_home_result", "full_time_guest_result", "date", "time", "venue", "status"], order_by="date asc")
			tournament.matches += frappe.get_all("Match", filters={"guest": self.name, "tournament": tournament.tournament}, fields=["name", "route", "home", "home_name", "guest", "guest_name", "full_time_home_result", "full_time_guest_result", "date", "time", "venue", "status"], order_by="date asc")	
			# Order the matches by date
			tournament.matches = sorted(tournament.matches, key=lambda k: k['date'])

		context.tournaments = tournaments

		# Get the club doctype of the team and add it to the context
		context.club = frappe.get_doc("Club", self.club)

		# Get the team rosters that are associated with the team filterred by role Player and add it to the context
		# Order by the position
		context.players = frappe.get_all("Team Roster", filters={"team": self.name, "role": "Player"}, fields=["name", "shirt_number", "person", "person.person_name", "person.picture", "person.route as person_route", "position", "position.position_name", "position.route as position_route"], order_by="position asc")

		# Get the team rosters that are associated with the team filterred by role Coach and add it to the context
		context.coaches = frappe.get_all("Team Roster", filters={"team": self.name, "role": "Coach"}, fields=["name", "shirt_number", "person", "person.person_name", "person.picture", "person.route as person_route", "position", "position.position_name", "position.route as position_route"], order_by="position asc")

		# Get the team rosters that are associated with the team filterred by role Staff and add it to the context
		# Order by the position
		context.staff = frappe.get_all("Team Roster", filters={"team": self.name, "role": "Staff"}, fields=["name", "shirt_number", "person", "person.person_name", "person.picture", "person.route as person_route", "position", "position.position_name", "position.route as position_route"], order_by="position asc")

	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()
			
def get_list_context(context=None):

	context.update(
		{
			"title": "Teams",
			"filters": {
				"owner": frappe.session.user
			}
		}		
	)

	# If the route is teams then get all the teams
	if frappe.local.request.path == "/teams":
		del context.filters["owner"]
