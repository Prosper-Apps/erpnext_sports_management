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
