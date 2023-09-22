# Copyright (c) 2023, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

import frappe

def after_install():
	create_user_roles()
	create_default_role_profiles()

def create_user_roles():
    # Check if the role exists
    if not frappe.db.exists("Role", "Sports User"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Sports User",
            "desk_access": 1,
            "restrict_to_domain": ""
        })
        role.insert(ignore_permissions=True)

    # Check if the role exists
    if not frappe.db.exists("Role", "Sports Manager"):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Sports Manager",
            "desk_access": 1,
            "restrict_to_domain": ""
        })
        role.insert(ignore_permissions=True)
	
def create_default_role_profiles():
	
    # Check if the role profile exists
    if not frappe.db.exists("Role Profile", "Sports"):
        for role_profile_name, roles in DEFAULT_ROLE_PROFILES.items():
            role_profile = frappe.new_doc("Role Profile")
            role_profile.role_profile = role_profile_name
            for role in roles:
                role_profile.append("roles", {"role": role})

            role_profile.insert(ignore_permissions=True)


DEFAULT_ROLE_PROFILES = {
	"Sports": [
		"Sports User",
		"Sports Manager",
	]	
}