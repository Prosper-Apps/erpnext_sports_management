# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TeamTournament(Document):
	def validate(self):
		if frappe.db.exists('Team Tournament', {'team': self.team, 'tournament': self.tournament}):
			frappe.throw(_('A tournament with the same team already exists.'))

	# After save of Team Tournament, create a new Ranking for the team in the tournament if it does not aleady exist
	def after_insert(self):
		if not frappe.db.exists('Ranking', {'team': self.team, 'tournament': self.tournament}):
			ranking = frappe.new_doc('Ranking')
			ranking.team = self.team
			ranking.tournament = self.tournament
			ranking.disabled = 1
			ranking.save(ignore_permissions=True)
			frappe.db.commit()
	

	# After delete of Team Tournament, disable the Ranking for the team in the tournament
	def on_trash(self):
		if frappe.db.exists('Ranking', {'team': self.team, 'tournament': self.tournament}):
			ranking = frappe.get_doc('Ranking', {'team': self.team, 'tournament': self.tournament})
			ranking.disabled = 1
			ranking.save(ignore_permissions=True)
			frappe.db.commit()

def get_list_context(context=None):

	context.update(
		{
			"filters": {
				"owner": frappe.session.user
			}
		}		
	)

	# If the route is teams then get all the teams
	if frappe.local.request.path == "/team-tournaments":
		del context.filters["owner"]
