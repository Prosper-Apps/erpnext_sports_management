# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Ranking(Document):
	def validate(self):
		validate_unique_ranking(self, "save")


def validate_unique_ranking(doc, method):
	# Check if the tournament and team link fields are set
	if doc.tournament and doc.team:
		# Check if there is another "Ranking" document with the same tournament and team link fields
		existing_doc = frappe.db.get_value("Ranking", {"tournament": doc.tournament, "team": doc.team})
		if existing_doc and existing_doc != doc.name:
			frappe.throw(_("A team can only participate in a tournament once"))
