# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class League(Document):
	def before_save(self):
		# Convert the short_name field to uppercase
		if self.short_name:
			self.short_name = self.short_name.upper()
