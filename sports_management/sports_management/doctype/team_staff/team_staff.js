// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team Staff', {
	refresh: function(frm) {
		// Limit the position column to only show the staff position
		frm.set_query("position", function() {
			return {
				"filters": [
					["Position", "role", "=", "Staff"]
				]
			};
		}
		);
	}
});
