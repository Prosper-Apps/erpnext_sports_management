# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.website.website_generator import WebsiteGenerator

class Match(WebsiteGenerator):

	def get_context(self, context):

		# Set the page title
		context.page_title = self.name

		# Set creadrumbs
		context.parents = [{'name': 'Home', 'route': '/'},  {'name': 'Matches', 'route': '/matches'}]

		context.tournament = frappe.get_doc('Tournament', self.tournament)
		context.game_day = frappe.get_doc('Game Day', self.game_day)
		context.home = frappe.get_doc('Team', self.home)
		context.home_club = frappe.get_doc('Club', context.home.club)
		context.guest = frappe.get_doc('Team', self.guest)
		context.guest_club = frappe.get_doc('Club', context.guest.club)
		if context.venue:
			context.venue = frappe.get_doc('Venue', self.venue)

		# Get the match rosters
		context.home_rosters = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.home, 'role': 'Player'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name', 'shirt_number', 'starting_lineup'], order_by='starting_lineup desc')
		context.guest_rosters = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.guest, 'role': 'Player'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name', 'shirt_number', 'starting_lineup'], order_by='starting_lineup desc')
		context.home_coaches = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.home, 'role': 'Coach'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name'], order_by='position desc')
		context.guest_coaches = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.guest, 'role': 'Coach'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name'], order_by='position desc')	
		context.home_staff = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.home, 'role': 'Staff'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name'], order_by='position desc')	
		context.guest_staff = frappe.get_list('Match Roster', filters={'match': self.name, 'team': self.guest, 'role': 'Staff'}, fields=['person', 'person.route as person_route', 'person_name', 'role', 'position', 'position.position_name'], order_by='position desc')

		# Get the match referees
		context.referees = frappe.get_list('Match Referee', filters={'match': self.name}, fields=['person', 'person.route as person_route', 'person.person_name', 'position', 'position.position_name'], order_by='position desc')

		# Get the match events
		context.events = frappe.get_list('Match Event', filters={'match': self.name}, fields=['events_type', 'match_roster', 'person_name', 'match_roster.team', 'match_roster.team_name', 'minute'], order_by='minute')

	# create function when saving a match to calculate the points for each team
	def on_update(self):
		frappe.call('sports_management.sports_management.doctype.tournament.tournament.calculate_rankings', self.tournament)

	# after insert create the match rosters
	def after_insert(self):
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
				match_roster_exists = frappe.db.exists('Match Roster', {'match': roster.match, 'person': roster.person, 'team': roster.team, 'role': roster.role, 'position': roster.position})
				if not match_roster_exists:	
					match_roster = frappe.new_doc('Match Roster')
					match_roster.person = roster.person
					match_roster.team = roster.team
					match_roster.role = roster.role
					match_roster.position = roster.position
					match_roster.shirt_number = roster.shirt_number
					match_roster.starting_lineup = roster.starting_lineup
					match_roster.match = self.name
					match_roster.save()
