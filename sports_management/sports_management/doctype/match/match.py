# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.website.website_generator import WebsiteGenerator

class Match(WebsiteGenerator):

	def get_context(self, context):
		# Get the venue, tournament, game day, home team and guest team aling with their name and route
		# Add all the data to the context to replace the existing
		if self.venue:
			context.venue = frappe.get_doc('Venue', self.venue)
		if self.tournament:
			context.tournament = frappe.get_doc('Tournament', self.tournament)
		if self.game_day:
			context.game_day = frappe.get_doc('Game Day', self.game_day)
		context.home = frappe.get_doc('Team', self.home)
		context.guest = frappe.get_doc('Team', self.guest)

	# create function when saving a match to calculate the points for each team
	def on_update(self):
		frappe.call('sports_management.sports_management.doctype.tournament.tournament.calculate_rankings', self.tournament)
		
		# create the match rosters
		self.create_match_rosters()

	# create a function that will create the match rosters based on the participating teams list of Team Rosters
	# For each Team Roster, create a Match Roster with the same person, team, role and position
	def create_match_rosters(self):
		# get the participating teams
		teams = [self.home, self.guest]
		# for each team, get the team roster
		for team in teams:
			team_roster = frappe.get_list('Team Roster', filters={'team': team}, fields=['person', 'team', 'role', 'position', 'starting_lineup'])
			# for each team roster, create a match roster
			for roster in team_roster:
				# Check if the match roster already exists for the same person, team, role and position
				# If it does, skip it
				match_roster_exists = frappe.db.exists('Match Roster', {'person': roster.person, 'team': roster.team, 'role': roster.role, 'position': roster.position})
				if not match_roster_exists:	
					match_roster = frappe.new_doc('Match Roster')
					match_roster.person = roster.person
					match_roster.team = roster.team
					match_roster.role = roster.role
					match_roster.position = roster.position
					match_roster.starting_lineup = roster.starting_lineup
					match_roster.match = self.name
					match_roster.save()
