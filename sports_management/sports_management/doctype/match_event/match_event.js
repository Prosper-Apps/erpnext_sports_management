// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Match Event', {

	// When the match is changed, refresh the frame
	match: function(frm) {

		// Limit the team to the team of the match
		frm.set_query("match_roster", function () {
			return {
				"filters": [
					["Match Roster", "match", "=", frm.doc.match]
				]
			};
		}); 
	},

	refresh: function(frm) {

		// Limit the match_roster to the match
		frm.set_query("match_roster", function () {
			return {
				"filters": [
					["Match Roster", "match", "=", frm.doc.match]
				]
			};
		}); 
	},

	// After save navigate back to the match
	after_save: function(frm) {
		frappe.set_route("Form", "Match", frm.doc.match);
	}

});

