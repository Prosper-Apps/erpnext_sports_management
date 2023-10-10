// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team Tournament', {
	// Limit the selection of tournaments to only those that have the same sports_type as the team
	refresh: function(frm) {
		frm.set_query("tournament", function() {
			return {
				filters: {
					sports_type: frm.doc.sports_type
				}
			};
		});
	},

});
