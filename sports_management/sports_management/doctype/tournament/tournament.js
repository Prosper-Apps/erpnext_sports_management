// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tournament', {
	refresh: function(frm) {
		if (!frm.doc.__islocal && frm.perm[0].write) {
			
			frm.add_custom_button(__('Create Matches'), function() {
				var tournament = frm.doc.name;
				frappe.confirm(
					__('Are you sure you want to create matches for this tournament? The old matches will be deleted.'),
					function(){
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
					},
					function(){
						// do nothing if user cancels
					}
				);
			});

			// Add a button that will delete the matches upon user confirmation
			frm.add_custom_button(__('Delete Matches'), function() {
				var tournament = frm.doc.name;
				frappe.confirm(
					__('Are you sure you want to delete the matches for this tournament?'),
					function(){
						frappe.call({
							method: 'sports_management.sports_management.doctype.tournament.tournament.delete_matches',
							args: {
								tournament: tournament
							},
							callback: function(r) {
								if (r.message) {
									frappe.msgprint(r.message);
								}
							}
						});
					},
					function(){
						// do nothing if user cancels
					}
				);
			});

			frm.add_custom_button(__('Calculate Rankings'), function() {
				var tournament = frm.doc.name;
				frappe.call({
					method: 'sports_management.sports_management.doctype.tournament.tournament.calculate_rankings',
					args: {
						tournament: tournament,
						send_message: true
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
