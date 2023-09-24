// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tournament', {
	refresh: function(frm) {
		if (!frm.doc.__islocal && frm.perm[0].write) {
			frm.add_custom_button(__('Create Matches'), function() {
				var tournament = frm.doc.name;
				frappe.call({
					method: 'sports_management.sports_management.doctype.tournament.tournament.create_matches',
					args: {
						tournament: tournament
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(r.message);
						}
					}
				});
			}).addClass('btn-primary');
		}
	}
});
