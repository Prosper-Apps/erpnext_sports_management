# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class MatchPerson(Document):
	def before_insert(self):
		if frappe.db.exists('Match Person', {'match': self.match, 'person': self.person, 'role': self.role}):
			frappe.throw(_('This person with same role is already part of this team.'))
