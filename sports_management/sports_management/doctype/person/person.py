# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator

class Person(WebsiteGenerator):
	def get_context(self, context):

		# Define the title of the page
		context.title = self.person_name

		# Define breadcrumbs
		context.parents = [{"name": "Home", "route":"/"}, {"name": "Persons", "route":"/persons"}]

		# Get a list of the teams that the person is a member of
		context.team_rosters = frappe.get_all("Team Roster", filters={"person": self.name}, fields=["team", "position", "role", "shirt_number"])

		# For each team get the team name and route
		for team_roster in context.team_rosters:
			team_roster.team_route = frappe.get_value("Team", team_roster.team, "route")
			team_roster.team_name = frappe.get_value("Team", team_roster.team, "team_name")
			team_roster.team_picture = frappe.get_value("Team", team_roster.team, "picture")
			team_roster.position_name = frappe.get_value("Position", team_roster.position, "position_name")
			team_roster.position_route = frappe.get_value("Position", team_roster.position, "route")

		# Get a list of all tournaments that are published
		context.tournaments = frappe.get_all("Tournament", filters={"published": 1}, fields=["route", "tournament_name", "picture", "regular_play_time"])
		for tournament in context.tournaments:

			# Get a list of all match rosters for the tournament that the person is a member of
			tournament.match_rosters = frappe.get_all("Match Roster", filters={"tournament": tournament.name, "person": self.name}, fields=["name", "tournament", "match", "team", "position", "role", "shirt_number", "starting_lineup"])	

			for match_roster in tournament.match_rosters:
				match_roster.match = frappe.get_doc("Match", match_roster.match)
				# Get a list of all match events for the match that the person is a member of
				match_roster.match_events = frappe.get_all("Match Event", filters={"match": match_roster.match.name, "match_roster": match_roster.name}, fields=["events_type", "minute"])
				
				# Calculate match_roster stats
				match_roster.stats = {}
				# Sum the goals scored by the person
				match_roster.stats['goals'] = len([event for event in match_roster.match_events if event.events_type == "Goal"])
				# Sub the own goals scored by the person
				match_roster.stats['own_goals'] = len([event for event in match_roster.match_events if event.events_type == "Own Goal"])
				# Sum the yellow cards received by the person
				match_roster.stats['yellow_cards'] = len([event for event in match_roster.match_events if event.events_type == "Yellow Card"])
				# Sum the red cards received by the person
				match_roster.stats['red_cards'] = len([event for event in match_roster.match_events if event.events_type == "Red Card"])
				# Get the substitute in minute from the match_roster.match_events
				substitute_in = [event.minute for event in match_roster.match_events if event.events_type == "Substitute In"]
				# if substitute_in is not empty then assign as zero
				if substitute_in:
					substitute_in = substitute_in[0]
				elif match_roster.starting_lineup == 0:
					substitute_in = tournament.regular_play_time
				else:
					substitute_in = 0
				# Get the substiture out minute from the match_roster.match_events
				substitute_out = [event.minute for event in match_roster.match_events if event.events_type == "Substitute Out"]
				if substitute_out:
					substitute_out = substitute_out[0]
				else:
					substitute_out = tournament.regular_play_time

				match_roster.stats['substitute_in'] = substitute_in
				match_roster.stats['substitute_out'] = substitute_out
				match_roster.stats['minutes_played'] = substitute_out - substitute_in

			# Calculate tournament stats
			tournament.stats = {}
			# Sum the appearances of the person
			tournament.stats['appearances'] = len(tournament.match_rosters)
			# Sum the goals scored by the person
			tournament.stats['goals'] = sum([match_roster.stats['goals'] for match_roster in tournament.match_rosters])
			# Sum the own goals scored by the person
			tournament.stats['own_goals'] = sum([match_roster.stats['own_goals'] for match_roster in tournament.match_rosters])
			# Sum the yellow cards received by the person
			tournament.stats['yellow_cards'] = sum([match_roster.stats['yellow_cards'] for match_roster in tournament.match_rosters])
			# Sum the red cards received by the person
			tournament.stats['red_cards'] = sum([match_roster.stats['red_cards'] for match_roster in tournament.match_rosters])
			# Sum the minutes played by the person
			tournament.stats['minutes_played'] = sum([match_roster.stats['minutes_played'] for match_roster in tournament.match_rosters])

			# Order tournament.match_rosters by match date
			tournament.match_rosters.sort(key=lambda x: x.match.date, reverse=False)

def get_list_context(context=None):

	context.update(
		{
			"show_sidebar": False,
			"show_search": True,
			"no_breadcrumbs": False,
			"title": _("Persons"),
			"parents": [{"name": "Home", "route":"/"}],
		}
	)
	