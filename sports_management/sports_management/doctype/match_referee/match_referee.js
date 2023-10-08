// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Match Referee', {
	// Limit the selection of positions to only those with role Referee
	refresh: function(frm) {
		frm.set_query("position", function() {
			return {
				filters: {
					"role": "Referee"
				}
			};
		});
	}
});
