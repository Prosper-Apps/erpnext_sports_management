// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ranking', {

	// When the tournament is changed update the teams filter
	tournament: function(frm) {

		// Set the team value to empty
		frm.set_value("team", "");
		
		// Refresh the frame
		frm.refresh();

	},

	refresh: function(frm) {

		// Get the tournament sports_type using frappe.db.get_value
		var tournament_sports_type = frappe.db.get_value("Tournament", frm.doc.tournament, "sports_type", function (r) {
			frm.set_query("team", function () {			

				return {
					"filters": [
						["Team", "sports_type", "=", r.sports_type]
					]
				};
			
			}
			);
		});

	}
});
