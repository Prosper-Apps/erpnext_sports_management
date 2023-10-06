# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TeamTournament(Document):
	def validate(self):
		if frappe.db.exists('Team Tournament', {'team': self.team, 'tournament': self.tournament}):
			frappe.throw(_('A tournament with the same team already exists.'))
