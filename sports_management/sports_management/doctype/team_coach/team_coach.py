# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TeamCoach(Document):
	def validate(self):
		if frappe.db.exists('Team Coach', {'team': self.team, 'person': self.person}):
			frappe.throw(_('A person with the same team already exists.'))
