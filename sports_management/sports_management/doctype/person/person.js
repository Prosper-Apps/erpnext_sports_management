// Copyright (c) 2023, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Person', {
	refresh: function(frm) {
		if (!frm.doc.__islocal && frm.perm[0].write) {
			frm.add_custom_button(__('Calculate Points'), function() {
				var person = frm.doc.name;
				frappe.call({
					method: 'sports_management.sports_management.doctype.person.person.calculate_person_points',
					args: {
						person: person
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(r.message);
						}
						frm.reload_doc();
					}
				});
			}).addClass('btn-primary');
		}
	}
});
