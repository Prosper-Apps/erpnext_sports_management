# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe

def asign_role_profile(doc, method):
    if doc.user_type == "Website User":
        doc.role_profile_name = "Sports"
        doc.save()

def asign_portal_user(doc, method):
    frappe.msgprint("Customer Updated")
    if doc.customer_type == "Individual":
        doc.append("portal_users", {"user": doc.email_id})
        doc.save()