// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team Personnel', {

	// When the role is changed if the role is player then show starting_lineup else hide
	role: function (frm) {
		// Set position value to empty
		frm.set_value("position", "");
		
		// If the role is player then show starting_lineup else hide
		if (frm.doc.role == "Player") {
			frm.toggle_display("starting_lineup", true);
			frm.set_value("starting_lineup", 1);
		} else {
			frm.toggle_display("starting_lineup", false);
			frm.set_value("starting_lineup", 0);
		}


	},

	// When the team is changed, update the positions
	team: function (frm) {

		// Set position value to empty
		frm.set_value("position", "");

		// Get the team sports type
		var sports_type = frappe.db.get_value("Team", frm.doc.team, "sports_type", function (r) {
			// Set the sports type
			frm.set_query("position", function () {			
				return {
					"filters": [
						["Position", "role", "=", frm.doc.role],
						["Position", "sports_type", "=", r.sports_type]
					]
				};
			}
			);
		});
	},

	refresh: function (frm) {
		// Limit the position column to only show the coach position
		frm.set_query("position", function () {			
			return {
				"filters": [
					["Position", "role", "=", frm.doc.role],
					["Position", "sports_type", "=", ""]
				]
			};
		}
		);
		
	}
});
