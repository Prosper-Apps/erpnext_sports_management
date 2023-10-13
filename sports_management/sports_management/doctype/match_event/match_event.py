# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MatchEvent(Document):
	# After inserting a new match event, update the match document
	# If the event is a goal, update the score
	def after_insert(self):
		match_doc = frappe.get_doc('Match', self.match)
		# Get team from match roster in the match event
		self.team = frappe.get_value('Match Roster', self.match_roster, ['team'])
		if self.events_type == "Goal":
			if self.team == match_doc.home:
				match_doc.full_time_home_result += 1
			else:
				match_doc.full_time_guest_result += 1
			match_doc.save()
		elif self.events_type == "Own Goal":
			if self.team == match_doc.home:
				match_doc.full_time_guest_result += 1
			else:
				match_doc.full_time_home_result += 1
			match_doc.save()
