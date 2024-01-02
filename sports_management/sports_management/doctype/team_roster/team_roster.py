# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TeamRoster(Document):
	def before_insert(self):
		if frappe.db.exists('Team Roster', {'team': self.team, 'person': self.person, 'role': self.role}):
			frappe.throw(_('This person with same role is already part of this team.'))

		# The maximun number of players in a team is 15
		# If the number of players is 15 then don't add the player
		# This is a validation
		if len(frappe.get_all('Team Roster', filters={'team': self.team})) == 15:
			frappe.throw(_('The maximun number of players in a team is 15.'))

def get_list_context(context=None):

	context.update(
		{
			"filters": {
				"owner": frappe.session.user
			}
		}		
	)

	# If the route is teams then get all the teams
	if frappe.local.request.path == "/team-rosters":
		del context.filters["owner"]
