# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TeamRoster(Document):
	def before_insert(self):
		if frappe.db.exists('Team Roster', {'team': self.team, 'person': self.person, 'role': self.position}):
			frappe.throw(_('This person with same position is already part of this team.'))

		# The maximun number of players in a team is 15
		# If the number of players is 15 then don't add the player
		# This is a validation
		if len(frappe.get_all('Team Roster', filters={'team': self.team})) == 15:
			frappe.throw(_('The maximun number of players in a team is 15.'))

		# Get all the team tournaments the team is part of,
		# loop throuh them and in case the tournament is published and doesn't allow team rosters then don't add the player
		for tournament in frappe.get_all('Team Tournament', filters={'team': self.team}, fields=['tournament_name', 'tournament']):		
			if frappe.db.exists('Tournament', {'name': tournament.tournament, 'published': 1, 'allow_team_roster': 0}):
				frappe.throw(_('The tournament {0} doesn\'t allow team rosters.'.format(tournament.tournament_name)))

	def before_save(self):
		# Get the position of the player and set it;s role to the team roster role
		self.role = frappe.get_value('Position', self.position, 'role')
		pass		

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
