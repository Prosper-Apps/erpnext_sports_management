# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class MatchReferee(Document):
	def before_insert(self):
		if frappe.db.exists('Match Referee', {'person': self.person}):
			frappe.throw(_('This person is already part of this match.'))
