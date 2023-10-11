# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Person(WebsiteGenerator):
	def get_context(self, context):

		# Get a list of the teams that the person is a member of
		context.team_rosters = frappe.get_all("Team Roster", filters={"person": self.name}, fields=["team", "position", "role", "shirt_number"])

		# For each team get the team name and route
		for team_roster in context.team_rosters:
			team_roster.team_route = frappe.get_value("Team", team_roster.team, "route")
			team_roster.team_name = frappe.get_value("Team", team_roster.team, "team_name")
			team_roster.team_picture = frappe.get_value("Team", team_roster.team, "picture")
			team_roster.position_name = frappe.get_value("Position", team_roster.position, "position_name")
			team_roster.position_route = frappe.get_value("Position", team_roster.position, "route")
